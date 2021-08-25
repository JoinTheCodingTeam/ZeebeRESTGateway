<script>
    import { createForm } from "svelte-forms-lib";
    import * as yup from "yup";

    const Method = Object.freeze({
        GET: "GET",
        POST: "POST",
        DELETE: "DELETE",
        PUT: "PUT",
        PATCH: "PATCH",
    });

    const ProtocolPrefix = Object.freeze({
        HTTP: "http://",
        HTTPS: "https://",
    });

    const VAR_REGEXP = /(?:(?:\$(\w+))|(?:\$\{(\w+)\}))/g;

    let fetching = false;
    let responseJSON = null;
    let responseError = null;

    let xmlError = null;
    let xmlDOM = null;
    let xmlIOMappings = [];
    let xmlText = null;

    const testKeyValueFilled = (item) => {
        return (
            (item.key == "" && item.value == "") ||
            (item.key.length > 0 && item.value.length > 0)
        );
    };

    const { form, errors, handleChange, handleSubmit } = createForm({
        initialValues: {
            method: Method.GET,
            protocolPrefix: ProtocolPrefix.HTTP,
            url: "",
            httpHeaders: [],
            variables: [],
        },
        validationSchema: yup.object().shape({
            method: yup.string().oneOf(Object.values(Method)),
            protocolPrefix: yup.string().oneOf(Object.values(ProtocolPrefix)),
            url: yup.string().required(),
            httpHeaders: yup.array().of(
                yup
                    .object()
                    .shape({
                        key: yup.string().ensure(),
                        value: yup.string().ensure(),
                    })
                    .test(
                        "bothFilled",
                        "Both fields should be filled",
                        testKeyValueFilled
                    )
            ),
            variables: yup.array().of(
                yup.object().shape({
                    key: yup.string().ensure(),
                    value: yup.string(),
                })
            ),
        }),
        onSubmit: async (values) => {
            fetching = true;
            responseJSON = null;
            responseError = null;
            const httpHeaders = values.httpHeaders
                .map(obj => ({key: obj.key, value: replaceVars(obj.value)}))
                .filter((obj) => obj.key && obj.value)
                .map((obj) => ({ [obj.key]: obj.value }));
            try {
                const url = replaceVars(values.url);
                console.log(url);
                const response = await fetch(values.protocolPrefix + url, {
                    method: values.method,
                    headers: Object.assign({}, ...httpHeaders),
                });
                responseJSON = await response.json();
            } catch (err) {
                responseError = err.toString();
            }
            fetching = false;
        },
    });

    const replaceVars = (str) => {
        return str.replaceAll(VAR_REGEXP, (_, m1, m2) => {
            const result = $form.variables.filter(
                (kv) => kv.key == (m1 || m2)
            )[0]?.value;
            console.log("!!", m1 || m2, result);
            return result !== undefined ? result : "";
        });
    };

    const handleUrlChange = (event) => {
        for (const prefix of Object.values(ProtocolPrefix)) {
            if (event.target.value.startsWith(prefix)) {
                const newUrl = event.target.value.substring(prefix.length);
                $form.url = newUrl;
                $form.protocolPrefix = prefix;
                return;
            }
        }
    };

    const handleHeaderChange = (i) => (event) => {
        const parts = event.target.value.split(":");
        if (parts.length < 2) {
            return;
        }
        $form.httpHeaders[i].key = parts[0].trim();
        $form.httpHeaders[i].value = event.target.value
            .substring(parts[0].length + 1)
            .trim();
    };

    const addHeader = () => {
        $form.httpHeaders = $form.httpHeaders.concat({ key: "", value: "" });
        $errors.httpHeaders = $errors.httpHeaders.concat({
            key: "",
            value: "",
        });
    };
    const removeHeader = (i) => () => {
        $form.httpHeaders = $form.httpHeaders.filter((_, j) => j !== i);
        $errors.httpHeaders = $errors.httpHeaders.filter((_, j) => j !== i);
    };

    const addVariable = () => {
        $form.variables = $form.variables.concat({ key: "", value: "" });
        $errors.variables = $errors.variables.concat({
            key: "",
            value: "",
        });
    };
    const removeVariable = (i) => () => {
        $form.variables = $form.variables.filter((_, j) => j !== i);
        $errors.variables = $errors.variables.filter((_, j) => j !== i);
    };

    const createDOM = () => {
        const dom = document.implementation.createDocument("", "", null);
        const root = dom.appendChild(
            dom.createElementNS(
                "http://www.omg.org/spec/BPMN/20100524/MODEL",
                "bpmn:root"
            )
        );
        root.setAttribute(
            "xmlns:zeebe",
            "http://www.omg.org/spec/BPMN/20100524/MODEL"
        );
        const extEl = root.appendChild(
            dom.createElement("bpmn:extensionElements")
        );
        const taskDef = extEl.appendChild(
            dom.createElement("zeebe:taskDefinition")
        );
        taskDef.setAttribute("type", "rest");
        extEl.appendChild(dom.createElement("zeebe:taskHeaders"));
        return dom;
    };

    function prettyFormatXML(xmlDoc) {
        const xsltDoc = new DOMParser().parseFromString(
            [
                '<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1">',
                '  <xsl:strip-space elements="*"/>',
                '  <xsl:template match="para[content-style][not(text())]">',
                '    <xsl:value-of select="normalize-space(.)"/>',
                "  </xsl:template>",
                '  <xsl:template match="node()|@*">',
                '    <xsl:copy><xsl:apply-templates select="node()|@*"/></xsl:copy>',
                "  </xsl:template>",
                '  <xsl:output indent="yes"/>',
                "</xsl:stylesheet>",
            ].join("\n"),
            "application/xml"
        );

        const xsltProcessor = new XSLTProcessor();
        xsltProcessor.importStylesheet(xsltDoc);
        return new XMLSerializer()
            .serializeToString(xsltProcessor.transformToDocument(xmlDoc))
            .split("\n")
            .slice(1, -1)
            .map((line) => line.substr(2))
            .join("\n");
    }

    function updateDomWithForm(form) {
        xmlDOM = createDOM();
        const headersEl = xmlDOM.getElementsByTagName("zeebe:taskHeaders")[0];

        const httpHeaders = form.httpHeaders
            .filter((obj) => obj.key && obj.value)
            .map((obj) => ({ [obj.key]: obj.value }));
        const headers = {
            method: form.method,
            url: form.protocolPrefix + form.url,
            headers: JSON.stringify(Object.assign({}, ...httpHeaders)),
        };
        for (const [key, value] of Object.entries(headers)) {
            const header = headersEl.appendChild(
                xmlDOM.createElement("zeebe:header")
            );
            header.setAttribute("key", key);
            header.setAttribute("value", value);
        }
        if (xmlIOMappings.length > 0) {
            const extEl = xmlDOM.getElementsByTagName(
                "bpmn:extensionElements"
            )[0];
            const mappingEl = extEl.appendChild(
                xmlDOM.createElement("zeebe:ioMapping")
            );
            for (const mapping of xmlIOMappings) {
                const child = mappingEl.appendChild(
                    xmlDOM.createElement(mapping.type)
                );
                child.setAttribute("source", mapping.source);
                child.setAttribute("target", mapping.target);
            }
        }
        xmlText = prettyFormatXML(xmlDOM);
    }
    $: updateDomWithForm($form);

    function handleXMLChange(event) {
        let content = event.target.value;
        let regex =
            /^\s*<bpmn:extensionElements>((.|[\r\n])*)<\/bpmn:extensionElements>\s*$/g;
        xmlDOM = null;
        xmlError = null;

        if (!content.match(regex)) {
            xmlError =
                "Root element should be the <bpmn:extensionElements> tag";
            return;
        }
        content =
            '<root xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"' +
            ' xmlns:zeebe="http://www.omg.org/spec/BPMN/20100524/MODEL">' +
            content +
            "</root>";
        const newDOM = new DOMParser().parseFromString(
            content,
            "application/xml"
        );
        const errors = newDOM.getElementsByTagName("parsererror");
        xmlError = errors.length > 0 ? errors[0].textContent + content : null;
        if (xmlError != null) {
            return;
        }

        const variables = [];
        const mappingEls = [
            ...newDOM.getElementsByTagName("zeebe:input"),
        ].concat([...newDOM.getElementsByTagName("zeebe:output")]);
        xmlIOMappings = mappingEls.map((el) => ({
            type: el.tagName,
            source: el.getAttribute("source"),
            target: el.getAttribute("target"),
        }));
        mappingEls.forEach((el) => {
            if (el.tagName == "zeebe:input") {
                variables.push(el.getAttribute("target"));
            }
        });

        const headers = newDOM.getElementsByTagName("zeebe:header");
        for (const header of headers) {
            const key = header.getAttribute("key");
            const value = header.getAttribute("value");
            if (key == "method") {
                $form.method = value;
            }
            if (key == "url") {
                const [prefix, url] = value.split("//", 2);
                $form.protocolPrefix = prefix + "//";
                $form.url = url;
                variables.push(
                    ...[...url.matchAll(VAR_REGEXP)].map((x) => x[1] || x[2])
                );
            }
            if (key == "headers") {
                $form.httpHeaders = Object.entries(JSON.parse(value)).map(
                    ([key, val]) => ({ key: key, value: val })
                );
                variables.push(
                    ...$form.httpHeaders
                        .map((el) =>
                            [...el.value.matchAll(VAR_REGEXP)].map(
                                (x) => x[1] || x[2]
                            )
                        )
                        .flat()
                );
            }
        }
        $form.variables = [...new Set(variables)].map((key) => ({
            key,
            value: "",
        }));
        updateDomWithForm($form);
    }

    function copyToClipboard() {
        const app = new CopyToClipboard({
            target: document.getElementById("clipboard"),
            props: { text: xmlText },
        });
        app.$destroy();
    }
</script>

<div>
    <form on:submit={handleSubmit}>
        <div>
            <select
                bind:value={$form.method}
                on:blur={handleChange}
                on:change={handleChange}
                disabled={fetching}
            >
                {#each Object.values(Method) as method}
                    <option value={method}>
                        {method}
                    </option>
                {/each}
            </select>

            <select
                bind:value={$form.protocolPrefix}
                on:blur={handleChange}
                on:change={handleChange}
                disabled={fetching}
            >
                {#each Object.values(ProtocolPrefix) as protocolPrefix}
                    <option value={protocolPrefix}>
                        {protocolPrefix}
                    </option>
                {/each}
            </select>

            <input
                placeholder="url"
                name="url"
                on:blur={handleUrlChange}
                on:change={handleUrlChange}
                on:input={handleUrlChange}
                bind:value={$form.url}
                disabled={fetching}
            />
        </div>
        <div>
            {#if $errors.method}
                <small class="error">{$errors.method}</small>
            {/if}
            {#if $errors.protocolPrefix}
                <small class="error">{$errors.protocolPrefix}</small>
            {/if}
            {#if $errors.url}
                <small class="error">{$errors.url}</small>
            {/if}
        </div>

        <p>
            Headers
            {#if $form.httpHeaders.length == 0}
                <button type="button" on:click={addHeader} disabled={fetching}
                    >+</button
                >
            {/if}
        </p>
        {#each $form.httpHeaders as _, j}
            <div class="form-group">
                <input
                    name={`httpHeaders[${j}].key`}
                    placeholder="name"
                    on:blur={handleHeaderChange(j)}
                    on:change={handleHeaderChange(j)}
                    on:input={handleHeaderChange(j)}
                    bind:value={$form.httpHeaders[j].key}
                    disabled={fetching}
                />
                <input
                    placeholder="value"
                    name={`httpHeaders[${j}].value`}
                    on:blur={handleHeaderChange(j)}
                    on:change={handleHeaderChange(j)}
                    on:input={handleHeaderChange(j)}
                    bind:value={$form.httpHeaders[j].value}
                    disabled={fetching}
                />
                <button
                    type="button"
                    on:click={removeHeader(j)}
                    disabled={fetching}>-</button
                >
                {#if j === $form.httpHeaders.length - 1}
                    <button
                        type="button"
                        on:click={addHeader}
                        disabled={fetching}>+</button
                    >
                {/if}
            </div>
            {#if $errors.httpHeaders[j] && typeof $errors.httpHeaders[j] == "string"}
                <small class="error">{$errors.httpHeaders[j]}</small>
            {/if}
            {#if $errors.httpHeaders[j]?.key}
                <small class="error">{$errors.httpHeaders[j].key}</small>
            {/if}
            {#if $errors.httpHeaders[j]?.value}
                <small class="error">{$errors.httpHeaders[j].value}</small>
            {/if}
        {/each}

        <p>
            Variables
            {#if $form.variables.length == 0}
                <button type="button" on:click={addVariable} disabled={fetching}
                    >+</button
                >
            {/if}
        </p>
        {#each $form.variables as _, j}
            <div class="form-group">
                <input
                    name={`variables[${j}].key`}
                    placeholder="name"
                    bind:value={$form.variables[j].key}
                    disabled={fetching}
                />
                <input
                    placeholder="value"
                    name={`variables[${j}].value`}
                    bind:value={$form.variables[j].value}
                    disabled={fetching}
                />
                <button
                    type="button"
                    on:click={removeVariable(j)}
                    disabled={fetching}>-</button
                >
                {#if j === $form.variables.length - 1}
                    <button
                        type="button"
                        on:click={addVariable}
                        disabled={fetching}>+</button
                    >
                {/if}
            </div>
            {#if $errors.variables[j] && typeof $errors.variables[j] == "string"}
                <small class="error">{$errors.variables[j]}</small>
            {/if}
            {#if $errors.variables[j]?.key}
                <small class="error">{$errors.variables[j].key}</small>
            {/if}
            {#if $errors.variables[j]?.value}
                <small class="error">{$errors.variables[j].value}</small>
            {/if}
        {/each}

        <div class="button-group">
            <button type="button" on:click={handleSubmit} disabled={fetching}
                >Fetch</button
            >
        </div>
    </form>

    <h1>Response</h1>
    {#if responseJSON != null}
        <pre>{JSON.stringify(responseJSON, null, 2)}</pre>
    {:else if responseError != null}
        <p class="error">{responseError}</p>
    {:else if fetching}
        <p>Fetching...</p>
    {:else}
        <p>&lt;None&gt;</p>
    {/if}

    <h1>Zeebe service task definition</h1>
    <div>
        <textarea
            name="xml"
            rows="10"
            cols="80"
            class:error={xmlError != null}
            on:input={handleXMLChange}
            on:change={handleXMLChange}
            on:blur={handleXMLChange}
            bind:value={xmlText}
            spellcheck="false"
            disabled={fetching}
        />
        {#if xmlError != null}
            <p class="error">{xmlError}</p>
        {/if}
        <div id="clipboard" />
        <button on:click={copyToClipboard}>Copy</button>
    </div>
</div>

<style>
    .error {
        display: block;
        color: red;
    }
    .form-group {
        display: flex;
        align-items: baseline;
    }
    .button-group {
        display: flex;
    }
    button ~ button {
        margin-left: 15px;
    }
</style>

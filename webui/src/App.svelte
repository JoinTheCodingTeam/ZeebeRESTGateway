<script>
    import { createForm } from "svelte-forms-lib";
    import { writable } from "svelte/store";
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

    const bothFilled = (item) => {
        return (
            (item.key == "" && item.value == "") ||
            (item.key.length > 0 && item.value.length > 0)
        );
    };

    const fetching = writable(false);
    const responseError = writable("");
    const responseJSONText = writable("");
    const { form, errors, handleChange, handleSubmit } = createForm({
        initialValues: {
            method: Method.GET,
            protocolPrefix: ProtocolPrefix.HTTP,
            url: "",
            headers: [],
            variables: [],
        },
        validationSchema: yup.object().shape({
            method: yup.string().oneOf(Object.values(Method)),
            protocolPrefix: yup.string().oneOf(Object.values(ProtocolPrefix)),
            url: yup.string().required(),
            headers: yup.array().of(
                yup
                    .object()
                    .shape({
                        key: yup.string().ensure(),
                        value: yup.string().ensure(),
                    })
                    .test(
                        "bothFilled",
                        "Both fields should be filled",
                        bothFilled
                    )
            ),
            variables: yup.array().of(
                yup
                    .object()
                    .shape({
                        key: yup.string().ensure(),
                        value: yup.string().ensure(),
                    })
                    .test(
                        "bothFilled",
                        "Both fields should be filled",
                        bothFilled
                    )
            ),
        }),
        onSubmit: async (values) => {
            $fetching = true;
            $responseError = "";
            $responseJSONText = "";
            const headers = values.headers
                .filter((obj) => (obj.key && obj.value))
                .map((obj) => ({ [obj.key]: obj.value }));
            try {
                const response = await fetch(
                    values.protocolPrefix + values.url,
                    {
                        method: values.method,
                        headers: Object.assign({}, ...headers),
                    }
                );
                $responseJSONText = await response.json();
            } catch (err) {
                $responseError = err.toString();
            } finally {
                $fetching = false;
            }
        },
    });

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

    const generateAdd = (arrayField) => () => {
        $form[arrayField] = $form[arrayField].concat({ key: "", value: "" });
        $errors[arrayField] = $errors[arrayField].concat({
            key: "",
            value: "",
        });
    };
    const generateRemove = (arrayField, i) => () => {
        $form[arrayField] = $form[arrayField].filter((_, j) => j !== i);
        $errors[arrayField] = $errors[arrayField].filter((_, j) => j !== i);
    };

    const addHeader = generateAdd("headers");
    const removeHeader = (i) => generateRemove("headers", i);
    const addVar = generateAdd("variables");
    const removeVar = (i) => generateRemove("variables", i);
</script>

<form on:submit={handleSubmit}>
    <div>
        <select
            bind:value={$form.method}
            on:blur={handleChange}
            on:change={handleChange}
            disabled={$fetching}
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
            disabled={$fetching}
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
            on:change={handleChange}
            on:blur={handleChange}
            on:change={handleUrlChange}
            bind:value={$form.url}
            disabled={$fetching}
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
        {#if $form.headers.length == 0}
            <button type="button" on:click={addHeader} disabled={$fetching}
                >+</button
            >
        {/if}
    </p>
    {#each $form.headers as _, j}
        <div class="form-group">
            <input
                name={`headers[${j}].key`}
                placeholder="name"
                on:change={handleChange}
                on:blur={handleChange}
                bind:value={$form.headers[j].key}
                disabled={$fetching}
            />
            <input
                placeholder="value"
                name={`headers[${j}].value`}
                on:change={handleChange}
                on:blur={handleChange}
                bind:value={$form.headers[j].value}
                disabled={$fetching}
            />
            <button
                type="button"
                on:click={removeHeader(j)}
                disabled={$fetching}>-</button
            >
            {#if j === $form.headers.length - 1}
                <button type="button" on:click={addHeader} disabled={$fetching}
                    >+</button
                >
            {/if}
        </div>
        {#if $errors.headers[j] && typeof $errors.headers[j] == "string"}
            <small class="error">{$errors.headers[j]}</small>
        {/if}
        {#if $errors.headers[j]?.key}
            <small class="error">{$errors.headers[j].key}</small>
        {/if}
        {#if $errors.headers[j]?.value}
            <small class="error">{$errors.headers[j].value}</small>
        {/if}
    {/each}

    <p>
        Variables
        {#if $form.variables.length == 0}
            <button type="button" on:click={addVar} disabled={$fetching}
                >+</button
            >
        {/if}
    </p>
    {#each $form.variables as _, j}
        <div class="form-group">
            <input
                name={`variables[${j}].key`}
                placeholder="name"
                on:change={handleChange}
                on:blur={handleChange}
                bind:value={$form.variables[j].key}
                disabled={$fetching}
            />
            <input
                placeholder="value"
                name={`variables[${j}].value`}
                on:change={handleChange}
                on:blur={handleChange}
                bind:value={$form.variables[j].value}
                disabled={$fetching}
            />
            <button type="button" on:click={removeVar(j)} disabled={$fetching}
                >-</button
            >
            {#if j === $form.variables.length - 1}
                <button type="button" on:click={addVar} disabled={$fetching}
                    >+</button
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
        <button type="button" on:click={handleSubmit} disabled={$fetching}
            >Try</button
        >
    </div>

    <small>{$responseError}</small>
    <pre>{JSON.stringify($responseJSONText, null, 2)}</pre>
</form>

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

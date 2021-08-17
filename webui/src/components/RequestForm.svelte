<script>
    import { createForm } from "svelte-forms-lib";
    import * as yup from "yup";
    import { Method, ProtocolPrefix } from "../utils/types";

    export let setFetching;
    export let setResponse;

    let fetching = false;

    const testKeyValueFilled = (item) => {
        return (
            (item.key == "" && item.value == "") ||
            (item.key.length > 0 && item.value.length > 0)
        );
    };
    const testValidJSON = (item) => {
        if (item == "") {
            return true;
        }
        try {
            JSON.parse(item);
        } catch {
            return false;
        }
        return true;
    };

    const { form, errors, handleChange, handleSubmit } = createForm({
        initialValues: {
            method: Method.GET,
            protocolPrefix: ProtocolPrefix.HTTP,
            url: "",
            headers: [],
            inputVariablesJSONText: "",
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
                        testKeyValueFilled
                    )
            ),
            inputVariablesJSONText: yup
                .string()
                .test("validJSON", "Should be valid JSON", testValidJSON),
        }),
        onSubmit: async (values) => {
            fetching = true;
            setFetching(true);
            setResponse(null, null);
            const headers = values.headers
                .filter((obj) => obj.key && obj.value)
                .map((obj) => ({ [obj.key]: obj.value }));
            try {
                const response = await fetch(
                    values.protocolPrefix + values.url,
                    {
                        method: values.method,
                        headers: Object.assign({}, ...headers),
                    }
                );
                setResponse(await response.json(), null);
            } catch (err) {
                setResponse(null, err.toString());
            }
            fetching = false;
            setFetching(false);
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

    const handleHeaderChange = (i) => (event) => {
        const parts = event.target.value.split(":");
        if (parts.length < 2) {
            return;
        }
        $form.headers[i].key = parts[0].trim();
        $form.headers[i].value = event.target.value
            .substring(parts[0].length + 1)
            .trim();
    };

    const addHeader = () => {
        $form.headers = $form.headers.concat({ key: "", value: "" });
        $errors.headers = $errors.headers.concat({
            key: "",
            value: "",
        });
    };
    const removeHeader = (i) => () => {
        $form.headers = $form.headers.filter((_, j) => j !== i);
        $errors.headers = $errors.headers.filter((_, j) => j !== i);
    };
</script>

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
        {#if $form.headers.length == 0}
            <button type="button" on:click={addHeader} disabled={fetching}
                >+</button
            >
        {/if}
    </p>
    {#each $form.headers as _, j}
        <div class="form-group">
            <input
                name={`headers[${j}].key`}
                placeholder="name"
                on:blur={handleHeaderChange(j)}
                on:change={handleHeaderChange(j)}
                on:input={handleHeaderChange(j)}
                bind:value={$form.headers[j].key}
                disabled={fetching}
            />
            <input
                placeholder="value"
                name={`headers[${j}].value`}
                on:blur={handleHeaderChange(j)}
                on:change={handleHeaderChange(j)}
                on:input={handleHeaderChange(j)}
                bind:value={$form.headers[j].value}
                disabled={fetching}
            />
            <button type="button" on:click={removeHeader(j)} disabled={fetching}
                >-</button
            >
            {#if j === $form.headers.length - 1}
                <button type="button" on:click={addHeader} disabled={fetching}
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

    <p>Variables</p>
    <textarea
        name="inputVariablesJSONText"
        rows="5"
        cols="80"
        on:change={handleChange}
        on:blur={handleChange}
        on:input={handleChange}
        bind:value={$form.inputVariablesJSONText}
        disabled={fetching}
    />
    {#if $errors.inputVariablesJSONText}
        <small class="error">{$errors.inputVariablesJSONText}</small>
    {/if}

    <div class="button-group">
        <button type="button" on:click={handleSubmit} disabled={fetching}
            >Fetch</button
        >
    </div>
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

<script>
    import RequestForm from "./components/RequestForm.svelte";
    import ZeebeXmlInput from "./components/ZeebeXMLInput.svelte";

    let fetching = false;
    let responseJSONText = null;
    let responseError = null;
    const setResponse = (resp, err) => {
        responseJSONText = resp;
        responseError = err;
    };
    const setFetching = (f) => {
        fetching = f;
    };
</script>

<RequestForm {setFetching} {setResponse} />

<h1>Response</h1>
{#if responseJSONText != null}
    <pre>{JSON.stringify(responseJSONText, null, 2)}</pre>
{:else if responseError != null}
    <p class="error">{responseError}</p>
{:else if fetching}
    <p>Fetching...</p>
{:else}
    <p>&lt;None&gt;</p>
{/if}

<h1>Zeebe service task definition</h1>
<ZeebeXmlInput name="xml" disabled={fetching} />

<style>
    .error {
        color: red;
    }
</style>

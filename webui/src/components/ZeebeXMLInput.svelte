<script>
    import { loop_guard } from "svelte/internal";

    import prettyFormatXML from "../prettyFormatXML";

    export let disabled = false;
    export let name;

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
        return dom;
    };

    let error = null;
    let dom = createDOM();
    $: xmlText = prettyFormatXML(dom);

    const handleChange = (event) => {
        const namespaces = {
            bpmn: "http://www.omg.org/spec/BPMN/20100524/MODEL",
            zeebe: "http://camunda.org/schema/zeebe/1.0",
        };
        const text = event.target.value;
        const index = text.search(/>/);
        const textWithNS =
            text.substring(0, index) +
            " " +
            Object.entries(namespaces)
                .map(([k, v]) => `xmlns:${k}="${v}"`)
                .join(" ") +
            text.substring(index);

        const newDOM = new DOMParser().parseFromString(
            textWithNS,
            "application/xml"
        );
        const errors = newDOM.getElementsByTagName("parsererror")
        console.log(errors.length, '!', textWithNS)
        error = errors.length > 0 ? errors[0].textContent : null;
        if (error == null) {
            dom = newDOM;
        }
    };
</script>

<div>
    <textarea
        {name}
        rows="10"
        cols="80"
        class:error={error != null}
        on:input={handleChange}
        on:change={handleChange}
        on:blur={handleChange}
        bind:value={xmlText}
        {disabled}
    />
    {#if error != null}
        <p class="error">{error}</p>
    {/if}
</div>

<style>
    .error {
        color: red;
    }
</style>

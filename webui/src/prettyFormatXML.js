export default function (xmlDoc) {
    const xsltDoc = new DOMParser().parseFromString([
        '<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1">',
        '  <xsl:strip-space elements="*"/>',
        '  <xsl:template match="para[content-style][not(text())]">',
        '    <xsl:value-of select="normalize-space(.)"/>',
        '  </xsl:template>',
        '  <xsl:template match="node()|@*">',
        '    <xsl:copy><xsl:apply-templates select="node()|@*"/></xsl:copy>',
        '  </xsl:template>',
        '  <xsl:output indent="yes"/>',
        '</xsl:stylesheet>',
    ].join('\n'), 'application/xml');

    const xsltProcessor = new XSLTProcessor();
    xsltProcessor.importStylesheet(xsltDoc);
    const resultDoc = xsltProcessor.transformToDocument(xmlDoc);
    return new XMLSerializer()
        .serializeToString(resultDoc)
        // .split('\n')
        // .slice(1, -1)
        // .map(line => line.substr(2))
        // .join('\n');
};

{/* <bpmn:extensionElements>
        <zeebe:taskDefinition type="rest" retries="3" />
        <zeebe:ioMapping>
          <zeebe:input source="= ctoTelegramId" target="telegramId" />
          <zeebe:output source="= response.length" target="responseLength" />
        </zeebe:ioMapping>
        <zeebe:taskHeaders>
          <zeebe:header key="headers" value="{&#34;Content-Type&#34;: &#34;application/json&#34;}" />
          <zeebe:header key="url" value="http://1" />
        </zeebe:taskHeaders>
      </bpmn:extensionElements> */}
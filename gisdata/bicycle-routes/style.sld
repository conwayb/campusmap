<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0"
                       xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
                       xmlns="http://www.opengis.net/sld"
                       xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xlink="http://www.w3.org/1999/xlink"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <NamedLayer>
        <Name>Bicycle Routes</Name>
        <UserStyle>
            <!-- Outline -->
            <FeatureTypeStyle>
                <Rule>
                    <LineSymbolizer>
                        <Stroke>
                            <CssParameter name="stroke">#474334</CssParameter>
                            <CssParameter name="stroke-width">4</CssParameter>
                            <CssParameter name="stroke-linecap">round</CssParameter>
                        </Stroke>
                    </LineSymbolizer>
                </Rule>
            </FeatureTypeStyle>

            <!-- Base/All -->
            <FeatureTypeStyle>
                <Rule>
                    <LineSymbolizer>
                        <Stroke>
                            <CssParameter name="stroke">#a8b400</CssParameter>
                            <CssParameter name="stroke-width">2</CssParameter>
                            <CssParameter name="stroke-linecap">round</CssParameter>
                        </Stroke>
                    </LineSymbolizer>
                </Rule>
            </FeatureTypeStyle>

            <!-- Medium Traffic -->
            <FeatureTypeStyle>
                <Rule>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>bike_there_classification</ogc:PropertyName>
                            <ogc:Literal>MT</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <LineSymbolizer>
                        <Stroke>
                            <CssParameter name="stroke">#e6dc8f</CssParameter>
                            <CssParameter name="stroke-width">2</CssParameter>
                            <CssParameter name="stroke-linecap">round</CssParameter>
                        </Stroke>
                    </LineSymbolizer>
                </Rule>
            </FeatureTypeStyle>

            <!-- High Traffic -->
            <FeatureTypeStyle>
                <Rule>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>bike_there_classification</ogc:PropertyName>
                            <ogc:Literal>HT</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <LineSymbolizer>
                        <Stroke>
                            <CssParameter name="stroke">#dc9b32</CssParameter>
                            <CssParameter name="stroke-width">2</CssParameter>
                            <CssParameter name="stroke-linecap">round</CssParameter>
                        </Stroke>
                    </LineSymbolizer>
                </Rule>
            </FeatureTypeStyle>

            <!-- Caution Area -->
            <FeatureTypeStyle>
                <Rule>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>bike_there_classification</ogc:PropertyName>
                            <ogc:Literal>CA</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <LineSymbolizer>
                        <Stroke>
                            <CssParameter name="stroke">#d2492a</CssParameter>
                            <CssParameter name="stroke-width">2</CssParameter>
                            <CssParameter name="stroke-linecap">round</CssParameter>
                        </Stroke>
                    </LineSymbolizer>
                </Rule>
            </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>

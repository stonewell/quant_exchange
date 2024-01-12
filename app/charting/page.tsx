"use client"

import dynamic from "next/dynamic";
import { useState } from "react";
import Script from "next/script";

import {
    ChartingLibraryWidgetOptions,
    ResolutionString,
} from "@/public/static/charting_library/charting_library";

const defaultWidgetProps: Partial<ChartingLibraryWidgetOptions> = {
    symbol: "sh000001",
    interval: "1D" as ResolutionString,
    library_path: "/static/charting_library/",
    locale: "en",
    fullscreen: false,
    autosize: true,
};

const TVChartContainer = dynamic(
    () =>
        import("@/components/TVChartContainer").then((mod) => mod.TVChartContainer),
    { ssr: false }
);

export default function Charting() {
    const [isScriptReady, setIsScriptReady] = useState(false);
    return (
        <>
            <Script
                src="/static/datafeeds/udf/dist/bundle.js"
                strategy="lazyOnload"
                onReady={() => {
                    setIsScriptReady(true);
                }}
            />
            {isScriptReady && <TVChartContainer {...defaultWidgetProps} />}
        </>
    )
}

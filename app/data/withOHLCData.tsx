import { tsvParse } from "d3-dsv";
import { timeParse } from "d3-time-format";
import * as React from "react";
import { IOHLCData } from "./iOHLCData";

const parseDate = timeParse("%Y-%m-%d");

const parseData = () => {
  return (d: any) => {
    const date = parseDate(d.d);
    if (date === null) {
      d.date = new Date(Number(d.d));
    } else {
      d.date = new Date(date);
    }

    for (const k in d) {
      var key = ''
      if (k === 'd')
        key = 'date'
      if (k === 'o')
        key = 'open'
      if (k === 'c')
        key = 'close'
      if (k === 'h')
        key = 'high'
      if (k === 'l')
        key = 'low'
      if (k === 'v')
        key = 'volume'

      if (key !== "date" && Object.prototype.hasOwnProperty.call(d, k)) {
        d[key] = +d[k];
      }
    }

    console.log(d);
    return d as IOHLCData;
  };
};

interface WithOHLCDataProps {
  readonly data: IOHLCData[];
}

interface WithOHLCState {
  data?: IOHLCData[];
  message: string;
}

export function withOHLCData(stockId = '', dataSet = "daily") {
  return <TProps extends WithOHLCDataProps>(OriginalComponent: React.ComponentClass<TProps>) => {
    return class WithOHLCData extends React.Component<Omit<TProps, "data">, WithOHLCState> {
      public constructor(props: Omit<TProps, "data">) {
        super(props);

        this.state = {
          message: `Loading ${dataSet} data...`,
        };
      }

      public componentDidMount() {
        fetch(
          `/api/stocks/${stockId}/${dataSet}`,
        )
          .then((response) => response.json())
          .then((data) => data.map(parseData()))
          .then((data) => {
            this.setState({
              data,
            });
          })
          .catch(() => {
            this.setState({
              message: `Failed to fetch data.`,
            });
          });
      }

      public render() {
        const { data, message } = this.state;
        if (data === undefined) {
          return <div className="center">{message}</div>;
        }

        return <OriginalComponent {...(this.props as TProps)} data={data} />;
      }
    };
  };
}

"use client"

import * as React from 'react';
import { Box, Divider } from '@mui/material';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepButton from '@mui/material/StepButton';
import Button from '@mui/material/Button';
import { FormProvider, useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import dayjs, { Dayjs } from 'dayjs';
import { LoadingButton } from '@mui/lab';

import { VictoryChart, VictoryLine, VictoryZoomContainer, VictoryTheme, VictoryLegend, VictoryAxis } from 'victory';

var utc = require('dayjs/plugin/utc')
dayjs.extend(utc)


import FormBackTest from './FormBackTest'
import FormSelectStock from './FormSelectStock'
import FormTrading from './FormTrading'
import FormRiskManagement from './FormRiskManagement'

const steps = ['回测', '选股', '买入卖出', '风险控制'];

function _renderStepContent(step: number) {
  switch (step) {
    case 1:
      return <FormBackTest />;
    case 2:
      return <FormSelectStock />;
    case 3:
      return <FormTrading />
    case 4:
      return <FormRiskManagement />
    default:
      return <span>Not Found</span>;
  }
}

const validationSchema = [
  // Form BackTest
  Yup.object().shape({
    initialCapital: Yup.number().positive().required().label('初始资金'),
    timeRangeFrom: Yup.date().required().label('起始回测时间'),
    timeRangeTo: Yup.date()
      .required().label('结束回测时间')
      .when('timeRangeFrom', ([timeRangeFrom], schema) => {
        if (timeRangeFrom) {
          return schema
            .min(timeRangeFrom, '结束回测时间不能小于开始时间');
        }

        return schema.min(0);
      }),
    frequent: Yup.string().required().label('回测频率'),
    baseline: Yup.string().required().label('回测基准'),
  }),
  // Form 2
  Yup.object().shape({
    stockSelectMethod: Yup.number().min(1).max(2).label('股票选择'),
    manualSelectedStocks: Yup.array().of(Yup.object())
      .when('stockSelectMethod', ([stockSelectMethod], schema) => {
        if (stockSelectMethod == 1) {
          return schema.min(2, '至少选择两支股票');
        }

        return schema.min(0);
      })
      .label('手选股票'),
  }),
  // Form 3
  Yup.object().shape({
    tradingMethod: Yup.number().min(1).max(2).label('买入卖出'),
    tradingInterval: Yup.number().min(1).label('调仓周期'),
    stockCount: Yup.number().min(1).label('最大持仓股票数'),
    buyMethod: Yup.number().min(1).max(2).label('买入方式'),
    sellStockWillBuy: Yup.number().min(0).max(2).label('卖出要买入股票'),
  }),
  Yup.object().shape({
    singleStockStopLoss: Yup.number().min(1).max(100).label('个股止损点'),
    indexStopLoss: Yup.number().min(1).label('沪深300平均止损点'),
  }),
];

export default function HorizontalNonLinearStepper() {
  const [activeStep, setActiveStep] = React.useState(0);
  const currentValidationSchema = validationSchema[activeStep];
  const [chartData, setChartData] = React.useState();

  const formProps = useForm({
    resolver: yupResolver(currentValidationSchema),
    defaultValues: {
      initialCapital: 100000,
      timeRangeFrom: dayjs().subtract(3, 'month'),
      timeRangeTo: dayjs(),
      frequent: 'D',
      baseline: 'sh000300',
      stockSelectMethod: 1,
      manualSelectedStocks: [],
      tradingMethod: 1,
      tradingInterval: 5,
      stockCount: 6,
      buyMethod: 1,
      sellStockWillBuy: 0,
      singleStockStopLoss: 20,
      indexStopLoss: 126,
    },
  });

  const { handleSubmit, control, formState } = formProps;

  const isLastStep = () => {
    return activeStep === steps.length - 1;
  };

  const onSubmit = async (value: any) => {
    const url = '/api/backtest/run';

    console.log(JSON.stringify(value));

    const postData = {
      initialCapital: value.initialCapital,
      timeRangeFrom: value.timeRangeFrom.utc().unix(),
      timeRangeTo: value.timeRangeTo.utc().unix(),
      frequent: value.frequent,
      baseline: value.baseline,
      stockSelectMethod: value.stockSelectMethod,
      manualSelectedStocks: value.manualSelectedStocks.map((s: any) => s.ticker),
      tradingMethod: value.tradingMethod,
      tradingInterval: value.tradingInterval,
      stockCount: value.stockCount,
      buyMethod: value.buyMethod,
      sellStockWillBuy: value.sellStockWillBuy,
      singleStockStopLoss: value.singleStockStopLoss,
      indexStopLoss: value.indexStopLoss,
    };

    await fetch(url, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData)
    })
      .then((res) => res.json())
      .then((data) => {
        console.log('value', data);
        setChartData(data);
      });
  };

  function _handleSubmit() {
    if (isLastStep()) {
      return handleSubmit(onSubmit)();
    } else {
      setActiveStep((prevActiveStep) => prevActiveStep + 1);
    }
  }

  function _handleBack() {
    if (activeStep === 0) {
      return;
    }
    setActiveStep(activeStep - 1);
  }


  const parentStyle: React.CSSProperties = {
    border: "1px solid #ccc",
    margin: "2%",
    maxWidth: "100%",
  };

  const BackTestChart = () => {
    const [width, setWidth] = React.useState(0);

    const graphRef = React.useCallback((node: any) => {
      if (node !== null) {
        setWidth(node.getBoundingClientRect().width);
      }
    }, []);

    const updateWidth = (ev: any) => {
      setWidth(ev.target.innerWidth);
    };

    React.useEffect(() => {
      window.addEventListener('resize', updateWidth);

      return () => {
        window.removeEventListener('resize', updateWidth);
      };
    }, []);

    return (
      <div ref={graphRef}>
        <VictoryChart
          width={width}
          height={400}
          theme={VictoryTheme.material}
          containerComponent={
            <VictoryZoomContainer
              responsive={false}
            />
          }
        >
          <VictoryLegend x={280} y={0}
            orientation="horizontal"
            gutter={50}
            style={{ title: { fontSize: 20 } }}
            data={[
              { name: "策略回报", symbol: { fill: "blue" } },
              { name: "基准回报", symbol: { fill: "purple" } }
            ]}
          />
          <VictoryLine
            style={{ data: { stroke: "blue" } }}
            data={chartData.custom}
          />
          <VictoryLine
            style={{ data: { stroke: "purple" } }}
            data={chartData.baseline}
          />
          <VictoryAxis
            dependentAxis />
          <VictoryAxis
            fixLabelOverlap={true} />
        </VictoryChart>
      </div>
    );
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Stepper nonLinear activeStep={activeStep}>
        {steps.map((label, index) => (
          <Step key={label}>
            <StepButton color="inherit" onClick={handleSubmit(() => setActiveStep(index))}>
              {label}
            </StepButton>
          </Step>
        ))}
      </Stepper>
      <Divider sx={{ mt: 4 }} />
      <FormProvider {...formProps}>
        <form onSubmit={handleSubmit(_handleSubmit)} >
          <div>
            <React.Fragment>
              {_renderStepContent(activeStep + 1)}
              <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
                <Button
                  color="inherit"
                  disabled={activeStep === 0}
                  onClick={_handleBack}
                  sx={{ mr: 1 }}
                >
                  上一步
                </Button>
                <Box sx={{ flex: '1 1 auto' }} />
                <LoadingButton
                  type='submit'
                  color='primary'
                  variant='contained'
                  loading={formState.isSubmitting}
                >
                  {isLastStep() ? '提交回测' : '下一步'}
                </LoadingButton>
              </Box>
            </React.Fragment>
          </div>
        </form>
      </FormProvider >
      {chartData && (
        <BackTestChart />
      )}
    </Box >
  );
}

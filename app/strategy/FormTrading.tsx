import * as React from 'react';

import { Stack } from '@mui/material';
import Typography from '@mui/material/Typography';

import { useFormContext, useWatch } from 'react-hook-form';

import FieldInputRadioGroup from '@/components/fields/FieldInputRadioGroup';
import FieldInputText from '@/components/fields/FieldInputText';
import FieldInputSelect from '@/components/fields/FieldInputSelect';

const buyMethods = [
  { label: '等比例买入', value: 1 },
  { label: '等量买入', value: 2 },
];

const yesNoOptions = [
  { label: '是', value: 1 },
  { label: '否', value: 0 },
];


function FormTrading() {
  const { control, getValues, setValue } = useFormContext();
  const tradingMethod = useWatch({
    control,
    name: "tradingMethod",
  });
  const [open, setOpen] = React.useState(false);

  const options = [
    {
      label: "轮动",
      value: 1,
    },
    /*
    {
      label: "择时",
      value: 2,
    },
     */
  ];

  return (
    <>
      <Stack gap={2}
        alignItems="stretch"
      >
        <FieldInputRadioGroup
          name='tradingMethod'
          control={control}
          label='买入卖出'
          options={options}
          onChangeHandler={(evt: any) => { }}
        />

        {tradingMethod == 1 && (
          <Stack gap={2}
            alignItems="stretch"
          >
            <FieldInputText
              name='tradingInterval'
              control={control}
              label='调仓周期（交易日）'
            />
            <FieldInputText
              name='stockCount'
              control={control}
              label='最大持仓股票数（只)'
            />
            <FieldInputSelect
              name='buyMethod'
              control={control}
              label='买入方式'
              options={buyMethods}
            />
            <FieldInputSelect
              name='sellStockWillBuy'
              control={control}
              label='卖出要买入股票'
              options={yesNoOptions}
            />
          </Stack>
        )}
        {tradingMethod == 2 && (
          <Typography>
            World
          </Typography>
        )}
      </Stack >
    </>
  );
}

export default FormTrading;

import React from 'react';
import { Stack } from '@mui/material';
import { useFormContext } from 'react-hook-form';
import FieldInputText from '@/components/fields/FieldInputText';
import FieldInputSelect from '@/components/fields/FieldInputSelect';
import FieldInputDatePicker from '@/components/fields/FieldInputDatePicker';

const backTestFrequents = [
  { label: '天', value: 'D' },
];
const backTestBaselines = [
  { label: '沪深300', value: 'HS300' },
];

function FormBackTest() {
  const { control } = useFormContext();

  return (
    <>
      <Stack gap={2}
        alignItems="stretch"
      >
        <FieldInputText
          name='initialCapital'
          control={control}
          label='初始资金'
        />
        <Stack direction="row"
          gap={2}
          alignItems="stretch"
        >
          <FieldInputDatePicker
            name='timeRangeFrom'
            label='起始回测时间'
            control={control}
          />
          <span>---</span>
          <FieldInputDatePicker
            name='timeRangeTo'
            label='结束回测时间'
            control={control}
          />
        </Stack>
        <FieldInputSelect
          name='frequent'
          label='回测频率'
          control={control}
          options={backTestFrequents}
        />
        <FieldInputSelect
          name='baseline'
          label='回测基准'
          control={control}
          options={backTestBaselines}
        />
      </Stack>
    </>
  );
}

export default FormBackTest;

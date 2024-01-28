import * as React from 'react';

import { Stack } from '@mui/material';

import { useFormContext, useWatch } from 'react-hook-form';

import FieldInputText from '@/components/fields/FieldInputText';


function FormRiskManagement() {
  const { control, getValues, setValue } = useFormContext();

  return (
    <>
      <Stack gap={2}
        alignItems="stretch"
      >
        <FieldInputText
          name='singleStockStopLoss'
          control={control}
          label='个股止损点（%）'
        />
        <FieldInputText
          name='indexStockLoss'
          control={control}
          label='沪深300平均止损点（日）'
        />
      </Stack >
    </>
  );
}

export default FormRiskManagement;

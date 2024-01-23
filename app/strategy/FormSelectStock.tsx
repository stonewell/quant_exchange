import * as React from 'react';
import { Stack } from '@mui/material';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';

import { useFormContext, useWatch } from 'react-hook-form';

import FieldInputRadioGroup from '@/components/fields/FieldInputRadioGroup';
import FieldInputList from '@/components/fields/FieldInputList';

function FormSelectStock() {
  const { control } = useFormContext();
  const stockSelectMethod = useWatch({
    control,
    name: "stockSelectMethod",
  });

  const options = [
    {
      label: "手动选股",
      value: 1,
    },
    {
      label: "指标选股",
      value: 2,
    },
  ];

  const onChange = (event: any) => {
    console.log('event', event);
  };

  return (
    <>
      <Stack gap={2}
        alignItems="stretch"
      >
        <FieldInputRadioGroup
          name='stockSelectMethod'
          control={control}
          label='股票选择'
          options={options}
          onChangeHandler={onChange}
        />

        {stockSelectMethod == 1 && (
          <Stack>
            <Box
              sx={{ width: '100%', maxHeight: 400, }}
            >
              <FieldInputList
                name="manualSelectedStocks"
                label="manualSelectedStocks"
                control={control}
                height={400}
              />
            </Box>
            <Box sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              '& > *': {
                m: 1,
              },
            }}
            >
              <ButtonGroup variant="contained" aria-label="">
                <Button>增加</Button>
                <Button>清除</Button>
              </ButtonGroup>
            </Box>
          </Stack>
        )}
        {stockSelectMethod == 2 && (
          <Typography>
            World
          </Typography>
        )}
      </Stack >
    </>
  );
}

export default FormSelectStock;
import * as React from 'react';
import { Stack } from '@mui/material';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';

import { useFormContext, useWatch } from 'react-hook-form';

import FieldInputRadioGroup from '@/components/fields/FieldInputRadioGroup';
import FieldInputList from '@/components/fields/FieldInputList';
import DialogStockSelect from '@/components/dialogs/DialogStockSelect';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import DeleteIcon from '@mui/icons-material/Delete';
import IconButton from '@mui/material/IconButton';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import ListItemButton from '@mui/material/ListItemButton';
import Avatar from '@mui/material/Avatar';
import { ListChildComponentProps } from 'react-window';

function FormSelectStock() {
  const { control, getValues, setValue } = useFormContext();
  const stockSelectMethod = useWatch({
    control,
    name: "stockSelectMethod",
  });
  const [open, setOpen] = React.useState(false);

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

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleDelete = (index: number) => {
    const manualSelectedStocks = getValues('manualSelectedStocks');

    manualSelectedStocks.splice(index, 1);
    setValue('manualSelectedStocks', manualSelectedStocks);
  };

  function renderRow(props: ListChildComponentProps) {
    const { index, style, data } = props;
    const length = data?.length ? data?.length : 0;

    if (index >= length) {
      return;
    }

    return (
      <ListItem
        style={style}
        key={index}
        component="div"
        disablePadding
        secondaryAction={
          <IconButton edge="end"
            aria-label="delete"
            onClick={() => { handleDelete(index); }}>
            <DeleteIcon />
          </IconButton>
        }
      >
        <ListItemButton
        >
          <ListItemAvatar>
            <Avatar>
              <ShowChartIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText
            primary={`${data[index].description}`}
            secondary={`${data[index].ticker}`}
          />
        </ListItemButton>
      </ListItem>
    );
  }

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
                renderRow={renderRow}
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
                <Button onClick={handleClickOpen}>增加</Button>
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
        <DialogStockSelect
          open={open}
          handleClose={handleClose}
        />
      </Stack >
    </>
  );
}

export default FormSelectStock;

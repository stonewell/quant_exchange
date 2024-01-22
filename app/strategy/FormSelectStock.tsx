import * as React from 'react';
import { Stack } from '@mui/material';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import FolderIcon from '@mui/icons-material/Folder';
import DeleteIcon from '@mui/icons-material/Delete';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';

import { useFormContext, useWatch } from 'react-hook-form';

import FieldInputRadioGroup from '@/components/fields/FieldInputRadioGroup';

import { FixedSizeList, ListChildComponentProps } from 'react-window';

function renderRow(props: ListChildComponentProps) {
  const { index, style } = props;

  if (index > 10)
    return;

  return (
    <ListItem
      style={style} key={index} component="div" disablePadding
      secondaryAction={
        <IconButton edge="end" aria-label="delete">
          <DeleteIcon />
        </IconButton>
      }
    >
      <ListItemAvatar>
        <Avatar>
          <FolderIcon />
        </Avatar>
      </ListItemAvatar>
      <ListItemText
        primary={`Single-line item:${index + 1}`}
      />
    </ListItem>
  );
}

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
              <FixedSizeList
                height={400}
                itemSize={46}
                itemCount={200}
                overscanCount={5}
              >
                {renderRow}
              </FixedSizeList>
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

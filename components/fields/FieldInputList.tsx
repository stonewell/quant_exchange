import React from 'react';
import { Stack } from '@mui/material';
import { Controller } from 'react-hook-form';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import DeleteIcon from '@mui/icons-material/Delete';
import IconButton from '@mui/material/IconButton';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';

import { FixedSizeList, ListChildComponentProps } from 'react-window';

type Props = {
    name: string;
    label: string;
    control: any;
    height: number;
};

function renderRow(value: any, props: ListChildComponentProps) {
    const { index, style } = props;
    const length = value?.length ? value?.length : 0;

    if (index >= length) {
        return;
    }

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
                    <ShowChartIcon />
                </Avatar>
            </ListItemAvatar>
            <ListItemText
                primary={`${value[index]}`}
            />
        </ListItem>
    );
}

function FieldInputList({ name, label, control, height }: Props) {
    return (
        <Controller
            name={name}
            control={control}
            render={({ field: { onChange, value }, fieldState: { error } }) => {
                return (
                    <Stack gap={2}
                        alignItems="stretch"
                    >
                        <FixedSizeList
                            height={height}
                            itemSize={46}
                            itemCount={value?.length ? value?.length : 0}
                            overscanCount={5}
                            fullWidth
                        >
                            {(props: ListChildComponentProps) => renderRow(value, props)}
                        </FixedSizeList>
                        {!!error && (
                            <Typography
                                color="error"
                            >
                                {`${error?.message ? error?.message : ''}`}
                            </Typography>
                        )}

                    </Stack>
                );
            }}
        />
    );
}

export default FieldInputList;

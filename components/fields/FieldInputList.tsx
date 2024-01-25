import React from 'react';
import { Stack } from '@mui/material';
import { Controller } from 'react-hook-form';
import Typography from '@mui/material/Typography';

import { FixedSizeList } from 'react-window';

type Props = {
    name: string;
    label: string;
    control: any;
    height: number;
    renderRow: any;
};


function FieldInputList({ name, label, control, height, renderRow }: Props) {
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
                            itemData={value}
                            overscanCount={5}
                            fullWidth
                        >
                            {renderRow}
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

import { TextField } from '@mui/material';
import { Controller } from 'react-hook-form';
import { DateRangePicker } from '@mui/x-date-pickers-pro/DateRangePicker';

type Props = {
    name: string;
    labelFrom: string;
    labelTo: string;
    control: any;
};

function FieldInputDateRangePicker({ name, labelFrom, labelTo, control }: Props) {
    return (
        <Controller
            name={name}
            control={control}
            render={({ field: { onChange, value }, fieldState: { error } }) => {
                return (
                    <DateRangePicker
                        onChange={onChange}
                        localeText={{ start: labelFrom, end: labelTo }}
                    />
                );
            }}
        />
    );
}

export default FieldInputDateRangePicker;

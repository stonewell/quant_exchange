import { TextField } from '@mui/material';
import { Controller } from 'react-hook-form';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

type Props = {
  name: string;
  label: string;
  control: any;
};

function FieldInputDatePicker({ name, label, control }: Props) {

  return (
    <Controller
      name={name}
      control={control}
      render={({ field: { onChange, value }, fieldState: { error } }) => {
        return (
          <DatePicker
            onChange={onChange}
            value={value}
            label={label}
            slotProps={{
              textField: {
                error: !!error,
                fullWidth: true,
                helperText: error?.message ? error?.message : '',
              },
            }}
          />
        );
      }}
    />
  );
}

export default FieldInputDatePicker;

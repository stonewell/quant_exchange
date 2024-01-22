import {
    FormControl,
    FormControlLabel,
    FormLabel,
    Radio,
    RadioGroup,
} from "@mui/material";
import { Controller } from "react-hook-form";

type Props = {
    name: string;
    label: string;
    control: any;
    options: any;
    onChangeHandler: any;
};

export const FormInputRadioGroup: React.FC<Props> = ({
    name,
    control,
    label,
    options,
    onChangeHandler,
}) => {
    const generateRadioOptions = (options: any) => {
        return options.map((singleOption: any) => (
            <FormControlLabel
                value={singleOption.value}
                label={singleOption.label}
                key={singleOption.value}
                control={<Radio />}
            />
        ));
    };
    return (
        <FormControl component="fieldset">
            <FormLabel component="legend">{label}</FormLabel>
            <Controller
                name={name}
                control={control}
                render={({
                    field: { onChange, value },
                    fieldState: { error },
                    formState,
                }) => (
                    <RadioGroup value={value} onChange={(event) => {
                        onChange(event);

                        if (onChangeHandler) {
                            onChangeHandler(event);
                        }
                    }} row>
                        {generateRadioOptions(options)}
                    </RadioGroup>
                )}
            />
        </FormControl>
    );
};

export default FormInputRadioGroup;

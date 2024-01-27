import * as React from 'react';

import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Divider from '@mui/material/Divider';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemButton from '@mui/material/ListItemButton';
import Avatar from '@mui/material/Avatar';
import Checkbox from '@mui/material/Checkbox';
import CircularProgress from '@mui/material/CircularProgress';
import Backdrop from '@mui/material/Backdrop';

import { useFormContext } from 'react-hook-form';
import { FixedSizeList, ListChildComponentProps } from 'react-window';

import { uniqueFetch } from '@/components/tools/UniqueFetch';

type Props = {
    handleClose: any;
    open: any;
};

export default function DialogStockSelect({ open, handleClose }: Props) {
    const [stocks, setStocks] = React.useState([]);
    const [checked, setChecked] = React.useState([]);
    const [loading, setLoading] = React.useState(false);

    const { setValue, getValues } = useFormContext();

    const handleToggle = (value: number) => () => {
        const currentIndex = checked.indexOf(value);
        const newChecked = [...checked];

        if (currentIndex === -1) {
            newChecked.push(value);
        } else {
            newChecked.splice(currentIndex, 1);
        }

        setChecked(newChecked);
    };

    function onSelectStocks() {
        if (checked.length == 0) {
            handleClose();
            setStocks([]);
            setChecked([]);
            return;
        }

        const manualSelectedStocks = getValues('manualSelectedStocks');
        const selectedStocks = checked.map((index) => stocks[index]);

        setValue('manualSelectedStocks', Array.from(new Set([...manualSelectedStocks, ...selectedStocks])));
        handleClose();
        setStocks([]);
        setChecked([]);
    }

    function onInputChange(event: any) {
        if (event?.target?.value === '') {
            return;
        }
        setLoading(true);
        uniqueFetch(`/api/udf/search?query=${event.target.value}&limit=20&type=&exchange=`,
            {
                signalKey: 'fetch-matched-symbols'
            }
        )
            .then((res) => res.json())
            .then((data) => {
                setStocks(data);
                setLoading(false);
            })
    }

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
                sx={{
                    backgroundColor: '#fafafa',
                    '&:not(:last-child)': {
                        borderBottom: '1px solid rgba(0, 0, 0, 0.12)',
                    },
                    '@media (hover: none)': {
                        '&:hover': {
                            backgroundColor: '#ff0000',
                        },
                    },
                    "&.Mui-selected": {
                        backgroundColor: "red"
                    },
                }}
                secondaryAction={
                    <ListItemText
                        primary={`${data[index].ticker}`}
                    />
                }
            >
                <ListItemButton
                    role={undefined}
                    onClick={handleToggle(index)}
                    sx={{
                        "&.Mui-selected": {
                            backgroundColor: '#F7921C'
                        },
                    }}
                >
                    <ListItemIcon>
                        <Checkbox
                            edge="start"
                            disableRipple
                            checked={checked.indexOf(index) !== -1}
                            tabIndex={-1}
                            inputProps={{ 'aria-labelledby': `checkbox-list-label-${index}` }}
                        />
                    </ListItemIcon>
                    <ListItemAvatar>
                        <Avatar>
                            <ShowChartIcon />
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                        primary={`${data[index].description}`}
                    />
                </ListItemButton>
            </ListItem>
        );
    }


    return (
        <React.Fragment>
            <Dialog
                open={open}
                onClose={handleClose}
                fullWidth
                disableRestoreFocus
                maxWidth="md"
            >
                <DialogTitle>股票</DialogTitle>
                <DialogContent sx={{
                    minHeight: 400,
                }}
                >
                    <DialogContentText>
                        输入股票代码或者名称缩写,在列表里选择对应的股票
                    </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="stock_id"
                        name="stock_id"
                        label="股票代码或者名称缩写"
                        fullWidth
                        variant="standard"
                        onChange={onInputChange}
                    />
                    <Divider />
                    <FixedSizeList
                        height={400}
                        itemSize={46}
                        itemData={stocks}
                        itemCount={stocks?.length ? stocks?.length : 0}
                        overscanCount={5}
                        fullWidth
                    >
                        {renderRow}
                    </FixedSizeList>
                    <Backdrop
                        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                        open={loading}
                    >
                        <CircularProgress color="inherit" />
                    </Backdrop>
                </DialogContent>
                <DialogActions>
                    <Button onClick={onSelectStocks}>确定</Button>
                </DialogActions>
            </Dialog>
        </React.Fragment >
    );
}

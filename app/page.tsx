import * as React from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Unstable_Grid2';
import Drawer from '@mui/material/Drawer';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Link from 'next/link';

export default function HomePage() {
    return (
        <Box sx={{ display: 'flex' }}>
            <div>
                <Grid container rowSpacing={3} columnSpacing={3}>
                    <Grid xs={6}>
                        <Link href='/charting'>历史行情</Link>
                    </Grid>
                    <Grid xs={6}>
                        <Link href='/strategy'>策略向导</Link>
                    </Grid>
                    <Grid xs={6}>
                    </Grid>
                    <Grid xs={6}>
                    </Grid>
                </Grid>
            </div>
        </Box>
    );
}

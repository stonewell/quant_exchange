import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

import { AppRouterCacheProvider } from '@mui/material-nextjs/v14-appRouter';
import { ThemeProvider } from '@mui/material/styles';
import Link from 'next/link';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Drawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DashboardIcon from '@mui/icons-material/Dashboard';
import HomeIcon from '@mui/icons-material/Home';
import StarIcon from '@mui/icons-material/Star';
import ChecklistIcon from '@mui/icons-material/Checklist';
import SettingsIcon from '@mui/icons-material/Settings';
import SupportIcon from '@mui/icons-material/Support';
import LogoutIcon from '@mui/icons-material/Logout';
import Stack from '@mui/material/Stack';
import Paper from '@mui/material/Paper';
import theme from '@/theme';

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'Quant Exchange - powered by TradingView',
    description: '',
}

const DRAWER_WIDTH = 240;

const LINKS = [
    { text: '首页', href: '/', icon: HomeIcon },
    { text: '历史行情', href: '/charting', icon: StarIcon },
    { text: '策略向导', href: '/strategy', icon: DashboardIcon },
];

const PLACEHOLDER_LINKS = [
    { text: 'Settings', icon: SettingsIcon },
    { text: 'Support', icon: SupportIcon },
    { text: 'Logout', icon: LogoutIcon },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body>
                <AppRouterCacheProvider options={{ enableCssLayer: true }}>
                    <ThemeProvider theme={theme}>
                        {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
                        <CssBaseline />

                        <Box sx=
                            {{
                                display: 'flex',
                                flexGrow: 1,
                                flexDirection: 'column',
                                height: '100vh',
                                p: 1,
                            }}
                        >
                            <Toolbar sx={{ backgroundColor: 'background.paper' }}>
                                <DashboardIcon sx={{ color: '#444', mr: 2, transform: 'translateY(-2px)' }} />
                                <Typography variant="h6" color="text.primary">
                                    Quant Exchange - powered by TradingView
                                </Typography>
                            </Toolbar>
                            <Divider />

                            <Box sx=
                                {{
                                    display: 'flex',
                                    flexGrow: 1,
                                    flexDirection: 'row',
                                    height: '100vh',
                                    p: 1,
                                }}
                            >
                                <Box
                                    sx={{
                                        display: 'flex',
                                        flexDirection: 'column',
                                        width: DRAWER_WIDTH,
                                        flexShrink: 0,
                                        boxSizing: 'border-box',
                                    }}
                                >
                                    <List>
                                        {LINKS.map(({ text, href, icon: Icon }) => (
                                            <ListItem key={href} disablePadding>
                                                <ListItemButton component={Link} href={href}>
                                                    <ListItemIcon>
                                                        <Icon />
                                                    </ListItemIcon>
                                                    <ListItemText primary={text} />
                                                </ListItemButton>
                                            </ListItem>
                                        ))}
                                    </List>
                                    <Box sx={{ flexGrow: 1 }}>
                                    </Box>
                                    <Paper variant="outlined"
                                        elevation={3}
                                        sx={{
                                        }}
                                    >
                                        <Typography variant="body2" color="text.primary"
                                            sx={{
                                                p: 2,
                                            }}
                                        >
                                            &nbsp;&nbsp;Quant Exchange uses <b>TradingView</b> technology to display trading data on charts.
                                            <br />&nbsp;&nbsp;<b>TradingView</b> is a charting platform for traders and investors, loved and visited by millions of users worldwide.
                                            <br />&nbsp;&nbsp;It offers state-of-the-art charting tools and a space where pepople driven by markets can track important upcoming events in the <a href='https://www.tradingview.com/economic-calendar/'>Economic calendar</a>, chat, chart, and prepare for trades.
                                        </Typography>
                                    </Paper>
                                    <List>
                                        {PLACEHOLDER_LINKS.map(({ text, icon: Icon }) => (
                                            <ListItem key={text} disablePadding>
                                                <ListItemButton>
                                                    <ListItemIcon>
                                                        <Icon />
                                                    </ListItemIcon>
                                                    <ListItemText primary={text} />
                                                </ListItemButton>
                                            </ListItem>
                                        ))}
                                    </List>
                                </Box>
                                <Box
                                    sx={{
                                        flexGrow: 1,
                                        display: 'flex',
                                        flexDirection: 'column',
                                        bgcolor: 'background.default',
                                        p: 1,
                                    }}
                                >
                                    {children}
                                </Box>
                            </Box>
                        </Box>
                    </ThemeProvider>
                </AppRouterCacheProvider>
            </body>
        </html >
    );
}

import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import "./Process.css";

const drawerWidth = 300;

const useStyles = makeStyles((theme) => ({
    drawer: {
        width: drawerWidth,
        flexShrink: 0,
    },
    drawerPaper: {
        width: drawerWidth,
    },
    drawerHeader: {
        display: 'flex',
        alignItems: 'center',
        padding: theme.spacing(0, 1),
        ...theme.mixins.toolbar,
        justifyContent: 'flex-end',
    },
}));

export default function PermanentDrawer(props) {
    const classes = useStyles();
    return (
        <Drawer
            className={classes.drawer}
            classes={{
                paper: classes.drawerPaper,
            }}
            anchor="left"
            open={props.open}
            variant="persistent"
        >
            <div className={classes.drawerHeader}>
                <IconButton onClick={() => props.trigger()}>
                    <ChevronLeftIcon />
                </IconButton>
            </div>
            <Divider />
            <div className="report">
                {props.report.map(info => {
                    return (
                        <div>{info}</div>
                    );
                })}
            </div>
        </Drawer>
    );
}
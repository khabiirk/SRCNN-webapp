import React, { useState } from 'react';
import './Navigation.css'
import 'bootstrap/dist/css/bootstrap.css';
import IconButton from '@material-ui/core/IconButton';
import GitHub from '@material-ui/icons/GitHub';

const Navigation = () => {
    document.body.style.backgroundColor = "#444";
    return (
        <nav className="navbar navbar-expand-lg">
            <div className="container-fluid">
                <a className="navbar-brand" href="#">SRCNN</a>

            </div>
            <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                    <li className="nav-item">
                     
                        
                        <label htmlFor="">
                            <IconButton aria-label="Github.com" color="primary" component="span" onClick = {() => window.open("https://github.com/khabiirk")}>
                                <GitHub/>
                            </IconButton>
        </label>
                    </li>
                </ul>
            </div>
        </nav>
    )
}

export default Navigation;
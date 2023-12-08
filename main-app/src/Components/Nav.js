import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import './Nav.css';

const Nav = () => {
  return (
    <div className="topnav">
      <NavLink exact to="/" activeClassName="active">
        HOME
      </NavLink>
      <NavLink exact to="/aboutus" activeClassName="active">
        ABOUT US
      </NavLink>
      <NavLink exact to="/fcm" activeClassName="active">
        FCM
      </NavLink>
      <NavLink exact to="/fcmParallel" activeClassName="active">
        FCM 2
      </NavLink>
    </div>
  );
};

export default Nav
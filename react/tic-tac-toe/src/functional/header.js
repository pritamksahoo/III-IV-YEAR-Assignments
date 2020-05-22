import React from 'react';
import '../css/header.css';
import icon from '../img/avatar.png';

const Header = (props) => {

    let dropdownList = () => {
        return (
            <div className="dropdown-div">
                <ul className="dropdown">
                    <li className="dropdown-item">Your Profile</li>
                    <li className="dropdown-item" ref={props.refLogOut} onClick={props.logout}>Log Out</li>
                </ul>
            </div>
        )
    }

    return (
        <div className="profile">
            <div className="profile-dropdown">
                <a className="dropdown-link">Welcome, {props.username}<b className="downward-arrow">&#8964;</b></a>
                
                <a className="alt-dropdown-link"><img className="profile-icon" src={icon} alt="alt" /><b className="downward-arrow"></b></a>
            </div>
            {dropdownList()}
        </div>
    )
}

export default Header;
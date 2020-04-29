import React, { Component } from 'react';
import { connect } from 'react-redux';

import * as actions from '../store/actions/actions';
import * as actionTypes from '../store/actions/actionTypes';

import history from './history';

class AuthCheck extends Component {

    componentDidMount() {
        if (this.props.auth.isAuthenticated()) {
            this.props.login_success()
            history.replace("/component/2")
        } else {
            this.props.login_failure()
            this.props.auth.handleLogOut()
            history.replace("/")
        }
    }

    render() {
        return (
            <div></div>
        )
    }
}

function mapStateToProps(state) {
    return {

    }
}

function mapDispatchToProps(dispatch) {
    return {
        login_success: () => {
            dispatch(actions.login_success())
        },
        login_failure: () => {
            dispatch(actions.login_failure())
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(AuthCheck);
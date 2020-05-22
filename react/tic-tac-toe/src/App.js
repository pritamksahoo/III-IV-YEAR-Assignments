import React, {Component} from 'react';
import axios from 'axios';
import { connect } from 'react-redux';
import { Route, Router, Switch, Link } from 'react-router-dom';
import * as actions from './store/actions/actions';
import history from './utils/history';

import Account from './containers/account';
import Boards from './containers/boards';
import Todos from './containers/todos';

import Header from './functional/header';
import RootRedirect from './functional/rootRedirect';

import './css/app.css';

class App extends Component {

	backend_api = 'https://todo-flask-backend.herokuapp.com/'

	constructor(props) {
		super(props)

		this.logOutBtn = React.createRef()
	}

	shouldComponentUpdate() {
		return true
	}

	handleLogOut = (username) => {

		this.logOutBtn.current.setAttribute("disabled", "disabled")
		this.logOutBtn.current.setAttribute("class", "dropdown-item clicked")

        axios.post(this.backend_api + 'logout/', {
            username: username
        })
        .then((result) => {
            let response = result.data
            let [text, status_code] = response
            if (status_code === 200) {
				this.props.logout(username)
				history.replace("/account/")
            } else {
				alert(text)
            }

            if (this.logOutBtn.current) {
				this.logOutBtn.current.removeAttribute("disabled")
        		this.logOutBtn.current.setAttribute("class", "dropdown-item")
        	}
        })
        .catch((err) => {
        	if (err) {
        		alert(err)
        		alert("Logout operation failed! Connection with server couldn't be extablished!")
        	}
        	if (this.logOutBtn.current) {
        		this.logOutBtn.current.removeAttribute("disabled")
        		this.logOutBtn.current.setAttribute("class", "dropdown-item")
        	}
        })
	}
	
	PrivateRoute = (pathTo, componentToRender) => {
        return (
            this.props.isAuthenticated === true 
            ? <Route exact path={pathTo} render={() => componentToRender} />
            : <Route exact path={pathTo} render={() => <Account login={true} message={''} />} />
        )
	}

	PrivateNoPropRoute = (pathTo, componentToRender) => {
        return (
            this.props.isAuthenticated === true 
            ? <Route exact path={pathTo} component={componentToRender} />
            : <Route exact path={pathTo} render={() => <Account login={true} message={''} />} />
        )
	}
	
	AuthRoute = (pathTo, componentToRender) => {
		// console.log("auth")
		return (
			this.props.isAuthenticated === false
			? <Route exact path={pathTo} render={() => componentToRender} />
			: <Route exact path="/boards" render={() => <Boards message={''} />} />
		)
	}

	render() {
		return (
			<div className="App">
				<Router history={history}>
					<div>
						<header className="common-header">
							<div className="logo">
								TODO
							</div>
							{
								this.props.isAuthenticated
								? <Header logout={() => this.handleLogOut(this.props.username)} refLogOut={this.logOutBtn} username={this.props.username} />
								: <Link className="header-login-link" to={{pathname: '/account/'}}>LogIn</Link>
							}
						</header>
						
						<Switch>

							<Route exact path="/" render={() => <RootRedirect {...this.props} />} />
							
							{this.AuthRoute("/account/", <Account login={true} message={''} />)}

							{this.PrivateRoute("/boards/", <Boards message={''} />)}

							{this.PrivateNoPropRoute("/boards/:todo", Todos)}
						</Switch>
					</div>
				</Router>
			</div>
		);
	}

	componentDidMount() {

	}
}

function mapStateToProps(state) {
	return {
		isAuthenticated: state.AuthReducer.isAuthenticated,
		username: state.AuthReducer.user
	}
}

function mapDispatchToProps(dispatch) {
	return {
		logout: (username) => {
			dispatch(actions.logout(username))
		}
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(App);

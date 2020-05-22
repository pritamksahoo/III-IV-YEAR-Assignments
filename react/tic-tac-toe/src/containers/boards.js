import React, { Component } from 'react';
import axios from 'axios';
import { connect } from 'react-redux';
import Config from '../utils/config';
import history from '../utils/history';
import { Link } from 'react-router-dom';

import '../css/boards.css';
// import * as actions from '../store/actions/actions';

class Boards extends Component {
    constructor(props) {
        super(props)

        this.state = {
            // isLogIn: props.login,
            message: props.message
        }

        this.createBoardBtn = React.createRef()

        // this.backend_api = 'http://192.168.43.183:8000/'
        this.backend_api = 'https://todo-flask-backend.herokuapp.com/'
    }

    getBoards = (username) => {

        if (this.props.isAuthenticated) {

            axios.post(this.backend_api + 'get_all_boards/', {
                username: username,
            }, Config)
            .then((result) => {
                let response = result.data
                console.log(response)
                let [text, status_code] = response

                if (status_code === 200) {
                    // console.log(text)
                    this.setState({
                        boards: text,
                        message: ''
                    })
                } else {
                    this.setState({
                        message: text
                    })
                }
            })
            .catch((err) => {

            })

        } else {
            history.replace("/")
        }
    }

    deleteBoard = (boardName, pos, id) => {
        let btn = document.getElementById(id)
        btn.setAttribute("disabled", "disabled")

        axios.post(this.backend_api + 'delete_board/', {
            username: this.props.username,
            board: boardName
        }, Config)
        .then((result) => {
            let response = result.data
            console.log(response)
            let [text, status_code] = response

            if (status_code === 200) {
                // console.log(text)
                this.setState({
                    // boards: text,
                    message: '',
                    boardDidDelete: true,
                    boardDidCreate: false,
                    intendedBoardIndex: pos
                })
            } else if (status_code === 404) {
                this.setState({
                    message: text
                })
            } else {
                this.setState({
                    message: text
                })
            }
            btn.removeAttribute("disabled")
        })
        .catch((err) => {
            if (err) {
                alert("Can't establish connection to server!")
            }
            btn.removeAttribute("disabled")
        })
    }

    createNewBoard = (event) => {
        event.preventDefault()
        let newBoard = event.target.newBoard.value

        this.createBoardBtn.current.setAttribute("disabled", "disabled")

        if (newBoard !== undefined && newBoard !== '') {
            axios.post(this.backend_api + 'create_new_board/', {
                username: this.props.username,
                board: newBoard
            }, Config)
            .then((result) => {
                let response = result.data
                console.log(response)
                let [text, status_code] = response

                if (status_code === 200) {
                    // console.log(text)

                    this.setState({
                        boards: text,
                        message: '',
                        boardDidCreate: true,
                        boardDidDelete: false,
                        intendedBoardIndex: 0
                    })
                } else if (status_code === 404) {
                    this.setState({
                        message: text
                    })
                } else {
                    this.setState({
                        message: text
                    })
                }

                this.createBoardBtn.current.removeAttribute("disabled")
            })
            .catch((err) => {
                if (err) {
                    alert("Can't establish connection to server!")
                }

                if (this.createBoardBtn.current) {
                    this.createBoardBtn.current.removeAttribute("disabled")
                }
            })
        }


    }

    createNewBoardForm = () => {
        this.setState({
            displayNewBoardForm: true
        })
    }

    hideNewBoardForm = () => {
        this.setState({
            displayNewBoardForm: false,
            message: ''
        })
    }

    newBoardForm = () => {
        return (
            <form onSubmit={this.createNewBoard}>
                <h4 className="form-header">CREATE NEW BOARD</h4><hr className="my-hr"></hr>

                <label>Board Name</label>
                <br></br>
                
                <input type="text" name="newBoard" placeholder="Enter new board name" id="newBoard" required/>
                <br></br>

                <button type="submit" ref={this.createBoardBtn}>Create</button>
            </form>
        )
    }

    toBeDeleted = (pos) => {
        let boards = this.state.boards
        // boards.pop(pos)
        // console.log("boards:before", boards)
        boards = [...boards.slice(0, pos), ...boards.slice(pos+1, boards.length)]

        // console.log("boards:after", boards)

        this.setState({
            boards: boards,
            boardDidDelete: false,
            boardDidCreate: false
        })
    }

    showBoards = () => {
        if (this.state.boards.length === 0) {
            return (
                <p>Board List Empty. Create One!</p>
            )
        }
        return (
            this.state.boards.map((item, pos) => {
                return (
                    <BoardItem key={`${pos}_${item[1]}`} id={`${pos}_${item[1]}`} item={item} pos={pos} 
                    
                    newlyCreated={this.state.boardDidCreate && this.state.intendedBoardIndex === pos ? true : false} 
                    
                    newlyDeleted={this.state.boardDidDelete && this.state.intendedBoardIndex === pos ? true : false}  

                    toBeDeleted={() => this.toBeDeleted(pos)}
                    
                    deleteBoard={() => this.deleteBoard(item[0], pos, `${pos}_${item[1]}`)} />
                )
            })
        )
    }

    shouldComponentUpdate() {
        return true
    }

    render() {
        return (
            <div className="main-board">
                <div className="topbar">
                    <div className="menu">
                        <span className="navigate inactive">BOARDS</span>
                    </div>
                </div>
                
                <p className="message">{this.state.message}</p><br></br>
                
                <div className="content">

                    <div className="createForm">
                        {this.newBoardForm()}
                    </div>

                    <div></div>

                    <div className="boards">
                        <h4 className="form-header board-header">ALL BOARDS</h4>

                        <h4 className="form-header alt-board-header">ALL BOARDS</h4>

                        <hr className="my-hr"></hr>
                        
                        {
                            this.state.boards 
                            ? this.showBoards()
                            : (
                                this.state.message
                                ? this.state.message
                                : "Retrieving Boards . . ."
                              )
                        }
                    </div>
                    
                </div>
            </div>
        )
    }

    componentDidMount() {
        this.getBoards(this.props.username)
    }
}

function mapStateToProps(state) {
    return {
        username: state.AuthReducer.user,
        'isAuthenticated': state.AuthReducer.isAuthenticated
    }
}

class BoardItem extends Component {

    constructor (props) {
        super(props)
        this.delBtn = React.createRef()
    }

    componentDidMount() {
        // document.addEventListener("click", this.closeMenu);
    }

    componentWillUnmount() {
        // let timeout = 2
    }

    componentDidUpdate() {
        // console.log("hello:", this.props.item[0], this.newlyDeleted)
        setTimeout(() => {
            if (this.props.newlyDeleted) {
                this.props.toBeDeleted()
            }
        }, 200)
    }

    // componentWillReceiveProps(newProps) {

    // }

    render () {
        // console.log(this.props.newlyCreated)
        return (
            <div className={"board-item " + (this.props.newlyCreated ? "new-board " : " " + (this.props.newlyDeleted ? "delete" : ""))}>
                <div className="left-span">
                    <Link className="board-link" to={{pathname: '/boards/' + this.props.item[0]}}>
                        {this.props.item[0]}
                    </Link><br></br><br></br>
                    <small><b>Created At : </b>{this.props.item[1]}</small>
                    
                </div>

                <div className="action-span">
                    <button id={this.props.id} className="del-button" onClick={() => { this.props.deleteBoard()}}>Del</button>
                </div>
            </div>
        )
    }
}

export default connect(mapStateToProps)(Boards);

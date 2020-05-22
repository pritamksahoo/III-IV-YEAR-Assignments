import React, { Component } from 'react';
import '../css/todos.css';

class TodoItem extends Component {

    componentDidUpdate () {
        // console.log(this.props.item[0])
        setTimeout(() => {
            if (this.props.newlyDeleted) {
                this.props.toBeDeleted()
            }
        }, 200)
    }

    render() {
        return (
            <div className={"todo-item " + (this.props.newlyCreated ? "new-todo " : " " + (this.props.newlyDeleted ? "delete " : ""))}>

                <div className="left-span">
                    <details>
                        <summary>{this.props.item[0]}</summary>
                        <br></br>
                        <small><b>Description : </b>{this.props.item[1]}</small><br></br>
                        <small><b>Last Modified : </b>{this.props.item[2]}</small>
                    </details>
                    
                </div>

                <div className="action-span">
                    <button id={this.props.id + "_del"} className="del-button" onClick={() => {this.props.deleteTodo()}}>Del</button>&nbsp;
                    {
                        !this.props.item[3]

                        ? <button id={this.props.id + "_complete"} className="flag-button" 
                        onClick={() => {this.props.completeTask()}}>
                            Complete
                        </button>

                        : <button id={this.props.id + "_incomplete"} className="flag-button" 
                        onClick={() => {this.props.inCompleteTask() }}>
                            Todo
                        </button>
                    }
                </div>
            </div>
        )
    }
}

export default TodoItem;

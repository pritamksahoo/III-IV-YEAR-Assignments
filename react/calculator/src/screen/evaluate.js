import React from 'react';
// import {digit} from '../keypad/digit';

export const evaluatePostfixExpression = (expr) => {
    let evalStack = []
    let ops = ['+', '-', '*', '/']

    for (let i=0; i<expr.length; i++) {
        let item = expr[i]
        if (ops.indexOf(item) >= 0) {
            let operand2 = evalStack.pop()
            let operand1 = evalStack.pop()
            let result = 0.0

            if (item === '+') {
                result = operand1 + operand2
            } else if (item === '-') {
                result = operand1 - operand2
            } else if (item === '*') {
                result = operand1 * operand2
            } else if (item === '/') {
                result = operand1 / operand2
            }

            evalStack.push(result)

        } else {
            evalStack.push(parseFloat(item))
        }

        // console.log(evalStack)
    }

    return evalStack[0]
}

export const evaluateByPostfixConversion = (expr) => {
    // let expr = expression.split(/[*+/-]+/)
    // console.log("Called once")
    let ops = ['+', '-', '*', '/']

    let tempStack = []
    let postfixStack = []
    let number = ""

    for (let i=0; i<expr.length; i++) {
        let item = expr[i]

        if (ops.indexOf(item) >= 0) {
            if (i === expr.length - 1) {
                break
            }

            postfixStack.push(number)
            number = ""

            if (tempStack.length === 0) {
                tempStack.push(item)
            } else {
                while (tempStack.length > 0 && (ops.indexOf(tempStack[tempStack.length - 1]) > ops.indexOf(item))) {
                    let popOp = tempStack.pop()
                    postfixStack.push(popOp)
                }

                tempStack.push(item)
            }
        } else {
            number = number + item
        }

    }

    postfixStack.push(number)

    while (tempStack.length > 0) {
        let popOp = tempStack.pop()
        postfixStack.push(popOp)
    }

    // console.log(postfixStack, tempStack)

    return evaluatePostfixExpression(postfixStack).toString()
}

export const evalExpr = (items, op) => {
    return items.reduce((ans, item, pos) => {
        if (op === '+') {
            return ans + parseFloat(item)
        } else if (op === '-') {
            return pos === 0 ? parseFloat(item) : (ans - parseFloat(item))
        } else if (op === '*') {
            return pos === 0 ? parseFloat(item) : (ans * parseFloat(item))
        } else if (op === '/') {
            return pos === 0 ? parseFloat(item) : (ans / parseFloat(item))
        }
    }, 0.0)
}

export const evaluate = (expr, op = ['+', '-', '*', '/'], index = 0) => {
    if (index === 4) {
        return expr
    } else {
        let exprParts = expr.split(op[index])
        
        let afterexprParts = exprParts.map((item, pos) => {
            return this.evaluate(item, op, index+1)
        })

        // console.log(afterexprParts, op[index])

        return this.evalExpr(afterexprParts, op[index])
    }
}
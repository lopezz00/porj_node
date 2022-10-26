import { pool } from '../db.js'

// Em retorna tots els users
export const getAllEmployees = async(req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM employee')
        res.json(rows)
    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}

// Em retorna un user un cop donada un id
export const getOneEmployees = async(req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM employee WHERE id = (?)', [req.params.id])

        if (rows.length <= 0) return res.status(404).json({
            message: "Employee not found"
        })
    
        res.json(rows[0])

    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}

// Creo un user un cop donat un json amb nom i salari
export const createEmployees = async (req, res) => {
    try {
        const {name, salary} = req.body
        const [rows] = await pool.query('INSERT INTO employee(name, salary) VALUES (?, ?)', [name, salary])
    
        res.send({id: rows.insertId, name, salary,
        })

    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}

// Elimino un usuari donat un id
export const deleteOneEmployee = async(req, res) => {
    try {
        const [result] = await pool.query('DELETE FROM employee WHERE id = (?)', [req.params.id])

        if (result.affectedRows <= 0) return res.status(404).json({
            message: "Employee not found"
        })
        res.sendStatus(204)

    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }

}



// Actualitza el salari , nom del usuari [id] en el cas de que li passem ,en el cas de que no, deixa el anterior
export const updateEmployees = async(req, res) => {
    try {
        const {id} = req.params
        const {name, salary} = req.body
    
        const [result] = await pool.query(
            'UPDATE employee SET name = IFNULL(?, name), salary = IFNULL(?, salary) WHERE id = (?)', [name, salary, id])
    
        if (result.affectedRows === 0) return res.status(404).json({
            message: "Employee not found"
        })
        res.sendStatus(204)
        console.log(id, name, salary)

    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}

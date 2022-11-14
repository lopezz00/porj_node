import { pool } from '../db.js'

// Em retorna tots els users
export const getAllUsers = async(req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM USUARI')
        res.json(rows)
    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}

// Em retorna un user un cop donadat un email
export const getOneUser = async(req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM USUARI WHERE email = (?)', [req.params.id])

        if (rows.length <= 0) return res.status(404).json({
            message: "Employee not found"
        })
    
        res.json(rows[0])

    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}
// Creo un user un cop donat un json amb email, nom i cognoms
export const createUser = async (req, res) => {
    try {
        const {email, nom, cognom1, cognom2} = req.body
        const [rows] = await pool.query('INSERT INTO user(email, name, cognom1, cognom2) VALUES (?, ?, ?, ?)', [email, nom, cognom1, cognom2])
    
        // s'hauria de comprovar la id per evitar ids iguals?? com es faria el pw??

        res.send({id: rows.insertId, email, nom, cognom1, cognom2,
        })

    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}
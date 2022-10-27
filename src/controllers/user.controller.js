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

// Em retorna un user un cop donada un id
export const getOneUser = async(req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM USUARI WHERE USUARI = (?)', [req.params.id])

        if (rows.length <= 0) return res.status(404).json({
            message: "Employee not found"
        })
    
        res.json(rows[0])

    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}
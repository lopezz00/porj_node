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
        const [rows] = await pool.query('SELECT * FROM USUARI WHERE email = (?)', [req.params.email])

        if (rows.length <= 0) return res.status(404).json({
            message: "Employee not found"
        })
    
        res.json(rows[0])


    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}

// Crea un user un cop donat un json amb email, nom i cognoms al body
// Comprovar pq no va.
// IMPORTANT : recorda afegir a user.routes.js per a poder cridar-ho i posar que es metode post
export const login = async (req, res) => {
    // Comprovar si els paramaters que rebem al body, estan ala bd.
    try {
        const {email, password} = req.body
        const [rows] = await pool.query(
            'SELECT id FROM USUARI where email = (?) and pw_hash = (?)', 
            [email, password]
        )
        
        if (length(rows) == 1) {
            // Carregar les cookies de usuari i dir que hem de anar a una nova pagina web
            res.json()
        }

    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong, unable to create user.'})
    }
}

// Update nom i cogonom d'un usuari donat un email en el body
export const updateUser = async(req, res) => {
    try {
        const {email} = req.params
        const {nom, cognom1} = req.body
    
        const [result] = await pool.query(
            'UPDATE USUARI SET nom = IFNULL(?, nom), cognom1 = IFNULL(?, cognom1) WHERE email = (?)',
            [nom, cognom1, email]
        )
    
        if (result.affectedRows === 0) return res.status(404).json({
            message: "Employee not found"
        })
        res.sendStatus(204)
        console.log(id, nom, cognom1)

    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}

// Elimina un usuari donat un email
export const deleteOneUser = async(req, res) => {
    try {
        const [result] = await pool.query('DELETE FROM USUARI WHERE email = (?)', [req.params.email])

        if (result.affectedRows <= 0) return res.status(404).json({
            message: "Employee not found"
        })
        res.sendStatus(204)

    } catch (e) {
        return res.status(500).json({message: 'Someting went wrong'})
    }
}
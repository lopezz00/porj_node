import { createPool } from "mysql2/promise"
import {
    DB_HOST,
    DB_PORT,
    DB_DATABASE,
    DB_USER,
    DB_PASSWORD
} from './config.js'

export const pool = createPool({
    host: DB_HOST, //Posariem la ip de la base de dades
    user: DB_USER,
    password: DB_PASSWORD,
    port: DB_PORT, // Per defecte
    database: DB_DATABASE

})
import { Router } from "express";
import { getAllUsers, getOneUser, login, deleteOneUser, updateUser } from '../controllers/user.controller.js'

const router = Router()

// Metodes GET
router.get('/user', getAllUsers)
router.get('/user/:email', getOneUser)

// Metodes POST
router.post('/user', login)

// Metodes PATCH
router.patch('/user/:email', updateUser)

// Metodes DELETE
router.delete('/user/:email', deleteOneUser)

export default router
import { Router } from "express";
import { getAllUsers, getOneUser, createUser, deleteOneUser } from '../controllers/user.controller.js'

const router = Router()

// Metodes GET
router.get('/user', getAllUsers)
router.get('/user/:email', getOneUser)

// Metodes POST
router.post('/user', createUser)

// Metodes PATCH
router.patch('/employees/:email', deleteOneUser)

// Metodes DELETE
router.delete('/employees/:email', deleteOneUser)

export default router
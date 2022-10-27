import { Router } from "express";
import { getAllUsers, getOneUser } from '../controllers/user.controller.js'

const router = Router()

router.get('/user', getAllUsers)

router.get('/user/:id', getOneUser)

export default router
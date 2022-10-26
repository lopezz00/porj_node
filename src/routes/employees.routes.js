import { Router } from "express";
import { createEmployees, deleteOneEmployee, getOneEmployees, getAllEmployees, updateEmployees } from '../controllers/employees.controller.js'

const router = Router()

router.get('/employees', getAllEmployees)

router.get('/employees/:id', getOneEmployees)

router.post('/employees', createEmployees)

router.delete('/employees/:id', deleteOneEmployee)

router.patch('/employees/:id', updateEmployees)

export default router
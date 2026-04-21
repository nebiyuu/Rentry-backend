import { Router } from "express";
import { requireAuth } from "../middlewares/auth.js";
import {
  createRentalOrder,
  getRentalOrder,
  getUserRentals,
  returnRental,
  cancelRental
} from '../controllers/rentalOrderController.js';
import { RentalOrder, Product, User } from '../models/index.js';
const router = Router();

// POST /api/rentals - Create rental order
router.post('/', requireAuth, createRentalOrder);

// GET /api/rentals - Get user's rentals
router.get('/', requireAuth, getUserRentals);

// GET /api/rentals/:orderId - Get specific rental
router.get('/:orderId', requireAuth, getRentalOrder);

// PUT /api/rentals/:orderId/return - Return rental
router.put('/:orderId/return', requireAuth, returnRental);

// PUT /api/rentals/:orderId/cancel - Cancel rental
router.put('/:orderId/cancel', requireAuth, cancelRental);

export default router;
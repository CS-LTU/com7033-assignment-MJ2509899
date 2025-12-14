/**
 * Unit Tests for API Service
 * 
 * Tests the frontend API functions including:
 * - Authentication endpoints (login/register)
 * - Patient data fetching
 * - Error handling
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { loginUser, registerUser, fetchPatients } from '../services/api';

// Mock fetch globally
global.fetch = vi.fn();

describe('API Service Tests', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    vi.resetAllMocks();
  });

  describe('loginUser', () => {
    it('should successfully login with valid credentials', async () => {
      const mockResponse = {
        token: 'mock-jwt-token',
        user: {
          id: 1,
          email: 'test@example.com',
          username: 'testuser',
          role: 'user'
        }
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await loginUser('test@example.com', 'password123');

      expect(result).toEqual(mockResponse);
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/auth/login',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: 'test@example.com', password: 'password123' })
        })
      );
    });

    it('should throw error on failed login', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        json: async () => ({ error: 'Invalid credentials' })
      });

      await expect(loginUser('wrong@example.com', 'wrongpass')).rejects.toThrow();
    });
  });

  describe('registerUser', () => {
    it('should successfully register a new user', async () => {
      const mockResponse = {
        token: 'mock-jwt-token',
        user: {
          id: 2,
          email: 'newuser@example.com',
          username: 'newuser',
          role: 'user'
        }
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await registerUser('newuser', 'newuser@example.com', 'password123', 'user');

      expect(result).toEqual(mockResponse);
      expect(result.user.role).toBe('user');
    });

    it('should successfully register a doctor', async () => {
      const mockResponse = {
        token: 'mock-jwt-token',
        user: {
          id: 3,
          email: 'doctor@example.com',
          username: 'doctor',
          role: 'doctor'
        }
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await registerUser('doctor', 'doctor@example.com', 'password123', 'doctor');

      expect(result.user.role).toBe('doctor');
    });
  });

  describe('fetchPatients', () => {
    it('should fetch all patients successfully', async () => {
      const mockPatients = [
        {
          id: 1,
          name: 'John Doe',
          age: 45,
          gender: 'Male',
          stroke_prediction: 0.25
        },
        {
          id: 2,
          name: 'Jane Smith',
          age: 50,
          gender: 'Female',
          stroke_prediction: 0.35
        }
      ];

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockPatients
      });

      const result = await fetchPatients('mock-token');

      expect(result).toEqual(mockPatients);
      expect(result).toHaveLength(2);
    });

    it('should include Authorization header', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });

      await fetchPatients('test-token');

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/patients/',
        expect.objectContaining({
          headers: expect.objectContaining({
            'Authorization': 'Bearer test-token'
          })
        })
      );
    });
  });
});

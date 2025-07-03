import { describe, it, expect } from 'vitest'
import type { Comment, UploadResponse } from './index'

describe('Types', () => {
  describe('Comment interface', () => {
    it('should have all required properties', () => {
      const comment: Comment = {
        id: '1',
        text: 'Test comment',
        location: 'Test location',
        created_at: '2023-01-01T00:00:00Z',
        image_url: 'https://example.com/image.jpg'
      }

      expect(comment.id).toBe('1')
      expect(comment.text).toBe('Test comment')
      expect(comment.location).toBe('Test location')
      expect(comment.created_at).toBe('2023-01-01T00:00:00Z')
      expect(comment.image_url).toBe('https://example.com/image.jpg')
    })

    it('should allow empty image_url', () => {
      const comment: Comment = {
        id: '2',
        text: 'Comment without image',
        location: 'Some location',
        created_at: '2023-01-01T00:00:00Z',
        image_url: ''
      }

      expect(comment.image_url).toBe('')
    })
  })

  describe('UploadResponse interface', () => {
    it('should have image_url property', () => {
      const response: UploadResponse = {
        image_url: 'https://example.com/uploaded-image.jpg'
      }

      expect(response.image_url).toBe('https://example.com/uploaded-image.jpg')
    })
  })
})
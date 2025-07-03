import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import CommentForm from './CommentForm'

// Mock axios
vi.mock('axios', () => ({
  default: {
    post: vi.fn()
  }
}))

describe('CommentForm', () => {
  it('renders form elements correctly', () => {
    render(<CommentForm />)
    
    expect(screen.getByText('Have you seen Tilit?')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Comment')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Location')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument()
  })

  it('updates input values when user types', async () => {
    const user = userEvent.setup()
    render(<CommentForm />)
    
    const commentInput = screen.getByPlaceholderText('Comment')
    const locationInput = screen.getByPlaceholderText('Location')
    
    await user.type(commentInput, 'Test comment')
    await user.type(locationInput, 'Test location')
    
    expect(commentInput).toHaveValue('Test comment')
    expect(locationInput).toHaveValue('Test location')
  })

  it('shows uploading state when form is submitted', async () => {
    const user = userEvent.setup()
    render(<CommentForm />)
    
    const commentInput = screen.getByPlaceholderText('Comment')
    const locationInput = screen.getByPlaceholderText('Location')
    const submitButton = screen.getByRole('button', { name: 'Submit' })
    
    await user.type(commentInput, 'Test comment')
    await user.type(locationInput, 'Test location')
    
    // Mock the axios post to be pending
    const axios = await import('axios')
    vi.mocked(axios.default.post).mockImplementation(() => new Promise(() => {}))
    
    await user.click(submitButton)
    
    expect(screen.getByText('Uploading...')).toBeInTheDocument()
    expect(submitButton).toBeDisabled()
  })

  it('requires both comment and location fields', () => {
    render(<CommentForm />)
    
    const commentInput = screen.getByPlaceholderText('Comment')
    const locationInput = screen.getByPlaceholderText('Location')
    
    expect(commentInput).toBeRequired()
    expect(locationInput).toBeRequired()
  })

  it('accepts file input for images', () => {
    render(<CommentForm />)
    
    // Find the file input directly by type
    const fileInput = document.querySelector('input[type="file"]')
    
    expect(fileInput).toBeInTheDocument()
    expect(fileInput).toHaveAttribute('accept', 'image/*')
  })

  it('calls onNewComment callback when provided', async () => {
    const mockCallback = vi.fn()
    const user = userEvent.setup()
    
    render(<CommentForm onNewComment={mockCallback} />)
    
    const commentInput = screen.getByPlaceholderText('Comment')
    const locationInput = screen.getByPlaceholderText('Location')
    const submitButton = screen.getByRole('button', { name: 'Submit' })
    
    await user.type(commentInput, 'Test comment')
    await user.type(locationInput, 'Test location')
    
    // Mock successful axios post
    const axios = await import('axios')
    vi.mocked(axios.default.post).mockResolvedValue({ data: {} })
    
    await user.click(submitButton)
    
    // Wait for the async operation to complete
    await new Promise(resolve => setTimeout(resolve, 0))
    
    expect(mockCallback).toHaveBeenCalled()
  })
})
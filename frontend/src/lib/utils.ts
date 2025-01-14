import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Combines and merges class names intelligently.
 *
 * @remarks
 * This utility function uses `clsx` to conditionally join class names and `tailwind-merge` to resolve potential Tailwind CSS class conflicts.
 *
 * @param inputs - Variable number of class name inputs that can be strings, objects, arrays, or conditionally rendered classes
 * @returns A merged string of class names with conflicting Tailwind classes resolved
 *
 * @example
 * cn('text-red-500', 'hover:text-blue-500')
 * cn({ 'bg-gray-100': isActive }, 'p-2', null)
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

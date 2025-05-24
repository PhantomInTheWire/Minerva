import { cn } from '@/lib/utils'
import { Card, CardDescription, CardTitle } from '@/components/ui/Card'
import { FilesIcon } from 'lucide-react'

interface EmptyCardProps extends React.ComponentPropsWithoutRef<typeof Card> {
  title: string
  description?: string
  action?: React.ReactNode
  icon?: React.ComponentType<{ className?: string }>
}

/**
 * Renders a stylized empty state card with an icon, title, optional description, and optional action element.
 *
 * @param title - The main heading displayed in the card.
 * @param description - Optional descriptive text shown below the title.
 * @param icon - Optional icon component to display; defaults to a generic files icon.
 * @param action - Optional React node rendered as an action element at the bottom of the card.
 *
 * @returns A React element representing the empty state card.
 */
export default function EmptyCard({
  title,
  description,
  icon: Icon = FilesIcon,
  action,
  className,
  ...props
}: EmptyCardProps) {
  return (
    <Card
      className={cn(
        'flex w-full flex-col items-center justify-center space-y-6 bg-transparent p-16',
        className
      )}
      {...props}
    >
      <div className="mr-4 shrink-0 rounded-full border border-dashed p-4">
        <Icon className="text-muted-foreground size-8" aria-hidden="true" />
      </div>
      <div className="flex flex-col items-center gap-1.5 text-center">
        <CardTitle>{title}</CardTitle>
        {description ? <CardDescription>{description}</CardDescription> : null}
      </div>
      {action ? action : null}
    </Card>
  )
}

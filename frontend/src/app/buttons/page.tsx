import React from 'react';
import OriginalButton from '@/components/ui/Button';
import { Button as CopiedButton } from '@/components/ui/button2'; // Assuming button2.tsx is the copied one

export default function ButtonsDemoPage() {
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Button Component Demo</h1>

      <div>
        <h2 className="text-lg font-semibold mb-2">Original Button (button.tsx)</h2>
        <OriginalButton>Original Click Me</OriginalButton>
        {/* Add more variants/examples if needed */}
      </div>

      <hr />

      <div>
        <h2 className="text-lg font-semibold mb-2">Copied Button (button2.tsx)</h2>
        {/* The copied button might have different props or usage */}
        {/* Check button2.tsx for correct usage */}
        <CopiedButton>Copied Click Me</CopiedButton>
        {/* Add more variants/examples if needed */}
      </div>
    </div>
  );
}
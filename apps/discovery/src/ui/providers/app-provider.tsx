'use client';
import type { FC, PropsWithChildren } from 'react';
import { ThemeProvider } from 'next-themes';

export const AppProvider: FC<PropsWithChildren> = (props) => {
  const { children } = props;
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
      {children}
    </ThemeProvider>
  );
};

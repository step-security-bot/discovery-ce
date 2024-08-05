'use client';
import { UserProfile } from '@clerk/nextjs';
import type { Theme } from '@clerk/types';
import { useTheme } from 'next-themes';
type Appearance = Record<'light' | 'dark', Theme>;
export default function Page() {
  const { resolvedTheme } = useTheme();
  const appearances: Appearance = {
    dark: {
      variables: {
        colorBackground: 'hsl(240, 10%, 3.9%)',
        colorNeutral: 'white',
        colorPrimary: 'hsl(0, 0%, 98%)',
        colorTextOnPrimaryBackground: 'hsl(240, 5.9%, 10%)',
        colorText: 'hsl(0, 0%, 98%)',
        colorInputText: 'hsl(240, 3.7%, 15.9%)',
        colorInputBackground: 'hsl(240, 3.7%, 15.9%)'
      },
      elements: {
        rootBox: {
          display: 'flex',
          flexDirection: 'column',
          width: '100%',
          padding: '0',
          boxShadow: 'none'
        },
        scrollBox: {
          boxShadow: 'none',
          background: 'transparent'
        },
        cardBox: {
          boxShadow: 'none',
          boxSizing: 'border-box',
          width: '100% !important'
        },
        navbar: {
          background: 'transparent'
        }
      }
    },
    light: {
      variables: {
        // colorBackground: 'transparent'
      },
      elements: {
        rootBox: {
          display: 'flex',
          flexDirection: 'column',
          width: '100%',
          padding: '0',
          boxShadow: 'none'
        },
        scrollBox: {
          boxShadow: 'none',
          background: 'transparent'
        },
        cardBox: {
          boxShadow: 'none',
          boxSizing: 'border-box',
          width: '100% !important'
        },
        navbar: {
          background: 'transparent'
        }
      }
    }
  };
  return (
    <UserProfile
      path="/dashboard/profile"
      appearance={appearances[resolvedTheme as 'light' | 'dark']}
    />
  );
}

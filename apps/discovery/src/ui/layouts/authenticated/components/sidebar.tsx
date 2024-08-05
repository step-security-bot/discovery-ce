'use client';

import { navItems } from '@/constants/data/nav-items';
import { NavItem } from '@/types';
import {
  Icons,
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger
} from '@discovery/shared/components';
import Link from 'next/link';
import { PropsWithChildren } from 'react';
export function RenderNavItem({ href, title, icon }: NavItem) {
  const Icon = Icons[icon];
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Link
          href={href}
          className="flex size-9 items-center justify-center rounded-lg bg-accent text-accent-foreground transition-colors hover:text-foreground md:size-8"
          prefetch={false}
        >
          <Icon className="size-5" />
          <span className="sr-only">{title}</span>
        </Link>
      </TooltipTrigger>
      <TooltipContent side="right">{title}</TooltipContent>
    </Tooltip>
  );
}

export function RenderMobileNavItem({ href, title, icon }: NavItem) {
  const Icon = Icons[icon];
  return (
    <Link
      href={href}
      className="flex items-center gap-4 px-2.5 text-muted-foreground hover:text-foreground"
      prefetch={false}
    >
      <Icon className="size-5" />
      <span className="sr-only">{title}</span>
    </Link>
  );
}
export function MobileSidebar() {
  return (
    <nav className="grid gap-6 text-lg font-medium">
      <Link
        href="#"
        className="group flex size-10 shrink-0 items-center justify-center gap-2 rounded-full bg-primary text-lg font-semibold text-primary-foreground md:text-base"
        prefetch={false}
      >
        <Icons.logo className="size-5 transition-all group-hover:scale-110" />
        <span className="sr-only">Discovery</span>
      </Link>
      {navItems
        .filter((item) => !item.disabled)
        .map((item) => (
          <RenderMobileNavItem key={item.href} {...item} />
        ))}
    </nav>
  );
}
export default function Sidebar({ children }: PropsWithChildren) {
  return (
    <aside className="fixed inset-y-0 left-0 z-10 hidden w-14 flex-col border-r bg-background sm:flex">
      <nav className="flex flex-col items-center gap-4 px-2 sm:py-5">
        <TooltipProvider>
          <Link
            href="#"
            className="group flex size-9 shrink-0 items-center justify-center gap-2 rounded-full bg-primary text-lg font-semibold text-primary-foreground md:size-8 md:text-base"
            prefetch={false}
          >
            <Icons.logo className="size-4 transition-all group-hover:scale-110" />
            <span className="sr-only">Discovery</span>
          </Link>
          {navItems
            .filter((item) => !item.disabled)
            .map((item) => (
              <RenderNavItem key={item.href} {...item} />
            ))}
        </TooltipProvider>
      </nav>
      <nav className="mt-auto flex flex-col items-center gap-4 px-2 sm:py-5">
        {children}
      </nav>
    </aside>
  );
}

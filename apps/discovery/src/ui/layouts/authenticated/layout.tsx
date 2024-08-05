import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
  Button,
  Icons,
  Input,
  Sheet,
  SheetContent,
  SheetTrigger
} from '@discovery/shared/components';
import dynamic from 'next/dynamic';
import Link from 'next/link';
import { PropsWithChildren } from 'react';
import Sidebar, { MobileSidebar } from './components/sidebar';
import { UserNav } from './components/user';

export default function AuthenticatedLayout({ children }: PropsWithChildren) {
  const ThemeToggle = dynamic(() => import('./components/theme-toggle'), {
    ssr: false
  });
  return (
    <div className="flex min-h-screen w-full flex-col bg-muted/40">
      <Sidebar>
        <ThemeToggle variant="tooltip" />
      </Sidebar>
      <div className="flex flex-col sm:ml-14">
        <header className="sticky top-0 flex h-14 items-center gap-4 border-b bg-background px-4 sm:h-20 sm:px-6">
          <Sheet>
            <SheetTrigger asChild>
              <Button size="icon" variant="outline" className="sm:hidden">
                <Icons.menu className="size-5" />
                <span className="sr-only">Toggle Menu</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="sm:max-w-xs">
              <MobileSidebar />
            </SheetContent>
          </Sheet>
          <Breadcrumb className="hidden md:flex">
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <Link href="#" prefetch={false}>
                    Dashboard
                  </Link>
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbPage>Bug Bounty</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
          <div className="relative ml-auto flex-1 md:grow-0">
            <Icons.search className="absolute left-2.5 top-2.5 size-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search..."
              className="w-full rounded-lg bg-background pl-8 md:w-[200px] lg:w-[336px]"
            />
          </div>
          <div className="flex items-center gap-2">
            <UserNav />
          </div>
        </header>
        <main className="flex-1 p-4">
          <div className="grid w-full grid-cols-1 gap-4 md:gap-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

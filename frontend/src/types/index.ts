export interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  role: string
  is_active: boolean
  avatar_url?: string
  phone?: string
  organization_id?: string
  last_login?: string
  created_at: string
  updated_at: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface Contact {
  id: string
  first_name: string
  last_name: string
  email?: string
  phone?: string
  mobile?: string
  job_title?: string
  department?: string
  status: string
  source: string
  address?: string
  city?: string
  state?: string
  country?: string
  zip_code?: string
  linkedin_url?: string
  twitter_handle?: string
  avatar_url?: string
  company_id?: string
  owner_id?: string
  organization_id?: string
  created_at: string
  updated_at: string
  tags: Tag[]
  company?: CompanyBrief
}

export interface CompanyBrief {
  id: string
  name: string
}

export interface Company {
  id: string
  name: string
  domain?: string
  industry?: string
  size?: string
  revenue?: number
  phone?: string
  email?: string
  website?: string
  description?: string
  address?: string
  city?: string
  state?: string
  country?: string
  zip_code?: string
  logo_url?: string
  employee_count?: number
  founded_year?: number
  owner_id?: string
  organization_id?: string
  created_at: string
  updated_at: string
}

export interface DealStage {
  id: string
  name: string
  order: number
  probability: number
  color: string
  organization_id?: string
  created_at: string
}

export interface Deal {
  id: string
  title: string
  value: number
  currency: string
  status: string
  priority: string
  description?: string
  expected_close_date?: string
  actual_close_date?: string
  probability: number
  stage_id?: string
  contact_id?: string
  company_id?: string
  owner_id?: string
  organization_id?: string
  lost_reason?: string
  created_at: string
  updated_at: string
  stage?: DealStage
}

export interface Activity {
  id: string
  type: string
  subject: string
  description?: string
  due_date?: string
  completed: boolean
  completed_at?: string
  duration_minutes?: number
  location?: string
  user_id: string
  contact_id?: string
  deal_id?: string
  organization_id?: string
  created_at: string
  updated_at: string
}

export interface Note {
  id: string
  content: string
  contact_id?: string
  deal_id?: string
  company_id?: string
  user_id: string
  organization_id?: string
  created_at: string
  updated_at: string
}

export interface Tag {
  id: string
  name: string
  color: string
  organization_id?: string
  created_at: string
}

export interface Notification {
  id: string
  type: string
  title: string
  message?: string
  read: boolean
  link?: string
  user_id: string
  created_at: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
  pages: number
}

export interface DashboardStats {
  total_contacts: number
  total_companies: number
  total_deals: number
  total_revenue: number
  won_deals: number
  lost_deals: number
  open_deals: number
  conversion_rate: number
  avg_deal_value: number
  pipeline_value: number
  activities_this_week: number
  new_contacts_this_month: number
}

export interface PipelineStage {
  id: string
  name: string
  order: number
  color: string
  probability: number
  deal_count: number
  total_value: number
}

export interface SearchResult {
  entity_type: string
  entity_id: string
  title: string
  subtitle?: string
  score: number
}

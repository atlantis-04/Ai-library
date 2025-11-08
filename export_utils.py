"""Utility functions for exporting reports"""

import pandas as pd
from datetime import datetime
from library_manager import LibraryManager

class ReportExporter:
    def __init__(self):
        self.manager = LibraryManager()
    
    def export_members_report(self, filename=None):
        """Export members data to CSV"""
        if filename is None:
            filename = f"members_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        members_df = self.manager.get_all_members()
        members_df.to_csv(filename, index=False)
        return filename
    
    def export_books_report(self, filename=None):
        """Export books inventory to CSV"""
        if filename is None:
            filename = f"books_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        books_df = self.manager.get_all_books()
        books_df.to_csv(filename, index=False)
        return filename
    
    def export_transactions_report(self, filename=None):
        """Export transaction history to CSV"""
        if filename is None:
            filename = f"transactions_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        transactions_df = self.manager.get_all_transactions()
        books_df = self.manager.get_all_books()
        members_df = self.manager.get_all_members()
        
        # Enrich with member and book names
        report = transactions_df.merge(
            members_df[['id', 'name']], 
            left_on='member_id', 
            right_on='id', 
            how='left'
        )
        report = report.merge(
            books_df[['id', 'title', 'author']], 
            left_on='book_id', 
            right_on='id', 
            how='left'
        )
        
        report = report[[
            'name', 'title', 'author', 'borrow_date', 
            'due_date', 'return_date', 'status', 'fine'
        ]]
        report.columns = [
            'Member', 'Book Title', 'Author', 'Borrowed Date',
            'Due Date', 'Return Date', 'Status', 'Fine ($)'
        ]
        
        report.to_csv(filename, index=False)
        return filename
    
    def export_overdue_report(self, filename=None):
        """Export overdue books report"""
        if filename is None:
            filename = f"overdue_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        transactions_df = self.manager.get_all_transactions()
        books_df = self.manager.get_all_books()
        members_df = self.manager.get_all_members()
        
        # Filter overdue
        overdue = transactions_df[
            (transactions_df['status'] == 'borrowed') & 
            (transactions_df['due_date'] < datetime.now())
        ]
        
        if overdue.empty:
            return None
        
        report = overdue.merge(
            members_df[['id', 'name', 'email']], 
            left_on='member_id', 
            right_on='id', 
            how='left'
        )
        report = report.merge(
            books_df[['id', 'title']], 
            left_on='book_id', 
            right_on='id', 
            how='left'
        )
        
        report['days_overdue'] = (datetime.now() - report['due_date']).dt.days
        report['expected_fine'] = report['days_overdue'] * self.manager.fine_per_day
        
        report = report[[
            'name', 'email', 'title', 'due_date', 'days_overdue', 'expected_fine'
        ]]
        report.columns = [
            'Member', 'Email', 'Book', 'Due Date', 'Days Overdue', 'Expected Fine ($)'
        ]
        
        report.to_csv(filename, index=False)
        return filename
    
    def export_all_reports(self):
        """Export all reports at once"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        reports = {
            'members': self.export_members_report(f"members_{timestamp}.csv"),
            'books': self.export_books_report(f"books_{timestamp}.csv"),
            'transactions': self.export_transactions_report(f"transactions_{timestamp}.csv"),
            'overdue': self.export_overdue_report(f"overdue_{timestamp}.csv")
        }
        
        return reports

if __name__ == "__main__":
    exporter = ReportExporter()
    reports = exporter.export_all_reports()
    print("📊 Reports exported:")
    for report_type, filename in reports.items():
        if filename:
            print(f"  ✓ {report_type}: {filename}")

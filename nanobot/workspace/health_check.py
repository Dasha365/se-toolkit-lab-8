#!/usr/bin/env python3
"""
Health check script for LMS backend monitoring.
This script checks for errors in the last 2 minutes and posts a summary.
"""

import sys
sys.path.append('/app/.venv/lib/python3.14/site-packages')

from nanobot.tools.mcp_obs_tools import logs_error_count, logs_search, traces_get
from nanobot.tools.mcp_lms_tools import lms_health
from nanobot.core.context import get_context
from nanobot.tools.message import message

def run_health_check():
    """Run the health check and post results to the chat."""
    
    # Check for errors in the last 2 minutes
    try:
        error_count_result = logs_error_count(
            service="Learning Management Service",
            time_window="2m"
        )
        
        error_count = error_count_result.get('error_count', 0)
        
        if error_count > 0:
            # Get the recent error logs
            logs_result = logs_search(
                query="_time:2m service.name:\"Learning Management Service\" severity:ERROR",
                limit=5
            )
            
            log_entries = logs_result.get('entries', [])
            
            if log_entries:
                # Extract trace_id from the most recent error log if available
                most_recent_log = log_entries[0] if log_entries else None
                trace_id = None
                
                if most_recent_log and 'trace_id' in most_recent_log:
                    trace_id = most_recent_log['trace_id']
                
                # Prepare summary message
                summary = f"⚠️ Health Check Alert: Found {error_count} errors in the last 2 minutes.\n\n"
                summary += f"Most recent error:\n"
                summary += f"- Timestamp: {most_recent_log.get('timestamp', 'N/A')}\n"
                summary += f"- Message: {most_recent_log.get('message', 'N/A')}\n"
                
                if trace_id:
                    try:
                        trace_result = traces_get(trace_id=trace_id)
                        if trace_result:
                            summary += f"\nTrace details for {trace_id}:\n"
                            summary += f"- Service: {trace_result.get('service', 'N/A')}\n"
                            summary += f"- Operation: {trace_result.get('operation', 'N/A')}\n"
                            summary += f"- Duration: {trace_result.get('duration', 'N/A')}ms\n"
                            
                            # Add any error details from the trace
                            if 'error' in trace_result:
                                summary += f"- Error: {trace_result['error']}\n"
                    except Exception as e:
                        summary += f"\nCould not retrieve trace details: {str(e)}"
                
                # Send the alert message
                message(content=summary)
            else:
                # Errors reported but no detailed logs found
                message(content=f"⚠️ Health Check Alert: Found {error_count} errors in the last 2 minutes, but couldn't retrieve detailed logs.")
        else:
            # No errors found, system looks healthy
            health_status = lms_health()
            status = health_status.get('status', 'unknown')
            item_count = health_status.get('item_count', 'unknown')
            
            message(content=f"✅ System Health Check: All good! No errors detected in the last 2 minutes. LMS Status: {status}, Items: {item_count}")
            
    except Exception as e:
        # Handle any errors in the health check itself
        error_msg = f"❌ Health Check Error: Could not complete health check - {str(e)}"
        message(content=error_msg)

if __name__ == "__main__":
    run_health_check()
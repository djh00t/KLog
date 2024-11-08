# examples/example.py

from klog import KLog

# Initialize KLog
log = KLog()

print(80 * "=")
print("Default template")
print(80 * "=")
# Log messages
log.info(
    message="System check completed successfully",
    reason="Plenty of space left",
    status="✅",
    template="default"
)

log.warning(
    message="Disk space running low",
    reason="Less than 10% space remaining",
    status="⚠️",
    template="default"
)

log.error(
    message="Failed to save file",
    reason="Permission denied",
    status="❌",
    template="default"
)

log.critical(
    message="Failed to save file",
    reason="Permission denied",
    status="🛑",
    template="default"
)

log.debug(
    message="Debugging application",
    reason="Variable x has unexpected value",
    status="🐛",
    template="default"
)

print()
print(80 * "=")
print("Basic Template")
print(80 * "=")

log.info(
    message="System check completed successfully",
    reason="Plenty of space left",
    template="basic"
)

log.warning(
    message="Disk space running low",
    reason="Less than 10% space remaining",
    template="basic"
)

log.error(
    message="Failed to save file",
    reason="Permission denied",
    template="basic"
)

log.critical(
    message="Failed to save file",
    reason="Permission denied",
    template="basic"
)

log.debug(
    message="Debugging application",
    reason="Variable x has unexpected value",
    template="basic"
)

print()
print(80 * "=")
print("None Template")
print(80 * "=")

log.info(
    message="INFO MESSAGE System check completed successfully",
    template="none"
)

log.warning(
    message="WARNING MESSAGE ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod"
    "tempor incididunt ut labore et dolore magna aliqua",
    template="none"
)

log.error(
    message="Error has occurred",
    reason="Error reason",
    template="none"
)

log.critical(
    message="Critical failure",
    status="CRITICAL",
    template="none"
)

log.debug(
    message="Debugging application",
    reason="Variable x has unexpected value",
    status="DEBUG",
    template="none"
)

print()
print(80 * "=")